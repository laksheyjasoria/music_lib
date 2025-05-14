# import os
# import requests

# class Redeployer:
#     """
#     A class to trigger redeployments on Railway via its GraphQL API.
#     """
#     GRAPHQL_URL = "https://api.railway.app/graphql"
#     REDEPLOY_MUTATION = """
#     mutation deploy($input: DeploymentCreateInput!) {
#       deploymentCreate(input: $input) {
#         id
#         status
#       }
#     }
#     """

#     def __init__(self):
#         # Read required environment variables
#         self.token = os.getenv("RAILWAY_API_TOKEN")
#         self.project_id = os.getenv("RAILWAY_PROJECT_ID")
#         self.service_id = os.getenv("RAILWAY_SERVICE_ID")  # optional for multi-service projects

#         if not self.token or not self.project_id:
#             raise RuntimeError("Missing RAILWAY_API_TOKEN or RAILWAY_PROJECT_ID environment variable")

#         # Prepare headers for GraphQL requests
#         self.headers = {
#             "Authorization": f"Bearer {self.token}",
#             "Content-Type": "application/json",
#         }

#     def trigger(self) -> dict:
#         """
#         Triggers a redeployment of the Railway project.

#         Returns:
#             dict: A response dict containing status and deployment details, e.g.
#                   {"status": "ok", "deploymentId": "...", "deploymentStatus": "..."}
#         """
#         # Build the variables payload
#         variables = {
#             "input": {
#                 "projectId": self.project_id,
#                 "trigger": "REDEPLOY"
#             }
#         }
#         # Include serviceId if provided
#         if self.service_id:
#             variables["input"]["serviceId"] = self.service_id

#         payload = {
#             "query": self.REDEPLOY_MUTATION,
#             "variables": variables
#         }

#         # Perform the GraphQL request
#         response = requests.post(self.GRAPHQL_URL, headers=self.headers, json=payload, timeout=10)
#         response.raise_for_status()
#         result = response.json()

#         # Check for errors in GraphQL response
#         if "errors" in result:
#             return {"status": "error", "errors": result["errors"]}

#         data = result.get("data", {}).get("deploymentCreate", {})
#         return {
#             "status": "ok",
#             "deploymentId": data.get("id"),
#             "deploymentStatus": data.get("status")
#         }

# # Singleton instance for easy import
# redeployer = Redeployer()


# redeployer.py
import os
import subprocess
import shlex

class RedeployerCLI:
    """
    Uses the official `railway` CLI to trigger a redeploy.
    """
    def __init__(self):
        # Ensure we have the required env vars
        self.project_id = os.getenv("RAILWAY_PROJECT_ID")
        token = os.getenv("RAILWAY_API_TOKEN")
        if not self.project_id or not token:
            raise RuntimeError("Missing RAILWAY_PROJECT_ID or RAILWAY_API_TOKEN")

        # Pass the token through RAILWAY_TOKEN so the CLI can pick it up
        os.environ["RAILWAY_TOKEN"] = token

    def trigger(self):
        """
        Runs `railway redeploy` for the configured project.
        Returns the CLI output or raises on error.
        """
        cmd = f"railway redeploy --project {shlex.quote(self.project_id)}"
        # If you need a specific service, append: --service SERVICE_ID

        try:
            result = subprocess.run(
                shlex.split(cmd),
                check=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            return {"status": "ok", "output": result.stdout.strip()}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "error": e.stderr.strip()}
        except Exception as e:
            return {"status": "error", "error": str(e)}

# Singleton instance
redeployer = RedeployerCLI()
