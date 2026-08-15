"""
Adaptive Mitigation Engine for DDoS Detection System.

This module provides adaptive response strategies based on the evaluated network risk level.
It receives a risk level string ("Low", "Medium", "High", "Critical") and returns
the appropriate mitigation action, description, and severity classification.
"""

def get_mitigation_action(risk_level: str):
    """
    Determines the appropriate mitigation strategy based on the input risk level.

    Parameters:
        risk_level (str): The calculated network risk level ("Low", "Medium", "High", "Critical").

    Returns:
        tuple: (mitigation_action, mitigation_description, severity)
            - mitigation_action (str): Specific defense action to execute.
            - mitigation_description (str): Human-readable explanation of the mitigation action.
            - severity (str): Severity classification level matching the risk assessment.
    """
    # Defensive mapping dictionary containing action, description, and severity for each risk level
    mapping = {
        "Low": {
            "action": "Monitor Traffic",
            "description": "Continue monitoring network activity.",
            "severity": "Low"
        },
        "Medium": {
            "action": "Rate Limiting",
            "description": "Apply traffic throttling to suspicious traffic.",
            "severity": "Medium"
        },
        "High": {
            "action": "Block Suspicious Traffic",
            "description": "Simulate blocking malicious traffic sources.",
            "severity": "High"
        },
        "Critical": {
            "action": "Emergency Defense",
            "description": "Simulate blocking traffic and triggering security alerts.",
            "severity": "Critical"
        }
    }

    # Retrieve corresponding strategy; default to Low monitoring if risk level is unknown
    details = mapping.get(risk_level, mapping["Low"])

    return details["action"], details["description"], details["severity"]
