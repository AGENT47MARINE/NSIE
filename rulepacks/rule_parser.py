import json
import math
from typing import Dict, Any, List
from app.models import RuleViolation, ValidationResult, LayoutCandidate, LayoutPlacement

class NavalRuleParser:
    def __init__(self, rulepack_path: str):
        """Loads the JSON rulepack into memory."""
        with open(rulepack_path, 'r') as f:
            data = json.load(f)
            self.version = data.get("version", "unknown")
            self.rules = data.get("rules", [])

    def evaluate(self, candidate: LayoutCandidate, components_metadata: Dict[str, Any]) -> ValidationResult:
        """
        Iterates through the JSON rules and applies the math to the candidate layout.
        """
        violations: List[RuleViolation] = []

        for rule in self.rules:
            rule_id = rule["rule_id"]
            severity = rule["severity"]
            params = rule["params"]
            
            # --- DISPATCHER: Route to the correct physics calculator based on the rule ID ---
            
            if rule_id == "MARPOL_TANK_001":
                # Dynamic Param: min_spacing_m (e.g., 0.76)
                v = self._check_tank_spacing(candidate.placements, components_metadata, params, severity, rule_id)
                if v: violations.extend(v)

            elif rule_id == "CLASS_GM_001":
                # Dynamic Params: gm_min_m, gm_max_m (e.g., 0.8, 3.5)
                v = self._check_stability_gm(candidate.placements, components_metadata, params, severity, rule_id)
                if v: violations.extend(v)
                
            elif rule_id == "SOLAS_EGRESS_001":
                # Egress clearance logic goes here
                pass 

        # If any rule triggered a 'hard' violation, the layout is dead.
        is_feasible = not any(v.severity.lower() == "hard" for v in violations)
        
        return ValidationResult(passed=is_feasible, violations=violations)

    # ---------------------------------------------------------
    # PHYSICS ENGINES (Driven by JSON params)
    # ---------------------------------------------------------

    def _check_tank_spacing(self, placements: List[LayoutPlacement], metadata: Dict[str, Any], 
                            params: dict, severity: str, rule_id: str) -> List[RuleViolation]:
        violations = []
        min_spacing = params.get("min_spacing_m", 0.0)
        
        # Filter placements to only look at fuel tanks
        tanks = [p for p in placements if metadata[p.component_id].hazard_class == 1] # Assuming 1 is Flammable
        
        for i, t1 in enumerate(tanks):
            for t2 in tanks[i+1:]:
                # Calculate 3D Euclidean distance between tank centers
                dist = math.sqrt(
                    (t1.position_xyz[0] - t2.position_xyz[0])**2 +
                    (t1.position_xyz[1] - t2.position_xyz[1])**2 +
                    (t1.position_xyz[2] - t2.position_xyz[2])**2
                )
                
                if dist < min_spacing:
                    violations.append(RuleViolation(
                        rule_id=rule_id,
                        severity=severity,
                        location=f"{t1.component_id} <-> {t2.component_id}",
                        message=f"MARPOL Violation: Tanks are {dist:.2f}m apart. Minimum is {min_spacing}m.",
                        evidence={"actual_distance": dist, "required_distance": min_spacing}
                    ))
        return violations

    def _check_stability_gm(self, placements: List[LayoutPlacement], metadata: Dict[str, Any], 
                            params: dict, severity: str, rule_id: str) -> List[RuleViolation]:
        violations = []
        gm_min = params.get("gm_min_m", 0.0)
        gm_max = params.get("gm_max_m", 99.0)
        
        total_mass = 0.0
        sum_mz = 0.0
        
        for p in placements:
            mass = metadata[p.component_id].mass_kg
            sum_mz += mass * p.position_xyz[2]  # Z-axis moment
            total_mass += mass
            
        if total_mass > 0:
            # Step 1: Calculate VCG (Vertical Center of Gravity)
            vcg = sum_mz / total_mass
            
            # Step 2: Calculate mock GM (Metacentric Height) 
            # GM = KM - VCG (Assuming KM is a constant 5.0 meters for this compartment's hull profile)
            KM = 5.0 
            gm = KM - vcg
            
            if gm < gm_min or gm > gm_max:
                violations.append(RuleViolation(
                    rule_id=rule_id,
                    severity=severity,
                    location="Global Stability",
                    message=f"CLASS Violation: GM is {gm:.2f}m. Must be between {gm_min}m and {gm_max}m.",
                    evidence={"actual_gm": gm, "gm_min": gm_min, "gm_max": gm_max, "vcg": vcg}
                ))
        return violations
