import requests
from django.http import JsonResponse

KEYCLOAK_URL = "http://keycloak:8080"
REALM = "universe-realm"
CLIENT_ID = "faculty-client"

def public_view(request):
    return JsonResponse({"message": "Faculty public endpoint"})

def protected_view(request):
    auth = request.headers.get("Authorization")
    if not auth:
        return JsonResponse({"error": "Missing token"}, status=401)

    token = auth.split()[1]

    userinfo = requests.get(
        f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )

    if userinfo.status_code != 200:
        return JsonResponse({"error": "Invalid token"}, status=403)

    data = userinfo.json()
    roles = data.get("resource_access", {}) \
                .get(CLIENT_ID, {}) \
                .get("roles", [])

    if "create_course" not in roles:
        return JsonResponse({"error": "Forbidden (faculty role missing)"}, status=403)

    return JsonResponse({
        "message": "Faculty protected data",
        "user": data["preferred_username"],
        "roles": roles
    })
