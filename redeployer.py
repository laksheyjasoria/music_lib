import os
import requests

class Redeployer:
    """
    A class to trigger redeployments on Railway via its GraphQL API.
    """
    GRAPHQL_URL = "https://backboard.railway.app/graphql"
    REDEPLOY_MUTATION = """
    mutation deploy($input: DeploymentCreateInput!) {
      deploymentCreate(input: $input) {
        id
        status
      }
    }
    """

    def __init__(self):
        # Read required environment variables
        self.token = os.getenv("RAILWAY_API_TOKEN")
        self.project_id = os.getenv("RAILWAY_PROJECT_ID")
        self.service_id = os.getenv("RAILWAY_SERVICE_ID")  # optional for multi-service projects

        if not self.token or not self.project_id:
            raise RuntimeError("Missing RAILWAY_API_TOKEN or RAILWAY_PROJECT_ID environment variable")

        # Prepare headers for GraphQL requests
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def trigger(self) -> dict:
        """
        Triggers a redeployment of the Railway project.

        Returns:
            dict: A response dict containing status and deployment details, e.g.
                  {"status": "ok", "deploymentId": "...", "deploymentStatus": "..."}
        """
        # Build the variables payload
        variables = {
            "input": {
                "projectId": self.project_id,
                "trigger": "REDEPLOY"
            }
        }
        # Include serviceId if provided
        if self.service_id:
            variables["input"]["serviceId"] = self.service_id

        payload = {
            "query": self.REDEPLOY_MUTATION,
            "variables": variables
        }

        # Perform the GraphQL request
        response = requests.post(self.GRAPHQL_URL, headers=self.headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        # Check for errors in GraphQL response
        if "errors" in result:
            return {"status": "error", "errors": result["errors"]}

        data = result.get("data", {}).get("deploymentCreate", {})
        return {
            "status": "ok",
            "deploymentId": data.get("id"),
            "deploymentStatus": data.get("status")
        }

# Singleton instance for easy import
redeployer = Redeployer()
