import requests
from django.http import JsonResponse

KEYCLOAK_URL = "http://keycloak:8080"
REALM = "universe-realm"
CLIENT_ID = "student-client"

def public_view(request):
    return JsonResponse({"message": "Student public endpoint"})
def protected_view(request):
    auth = request.headers.get("Authorization")

    # 1️⃣ Check header exists
    if not auth:
        return JsonResponse({"error": "Authorization header missing"}, status=401)

    parts = auth.split()

    # 2️⃣ Check format: "Bearer <token>"
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return JsonResponse(
            {"error": "Invalid Authorization header format"},
            status=401
        )

    token = parts[1]

    # 3️⃣ Call Keycloak userinfo
    resp = requests.get(
        f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )

    if resp.status_code != 200:
        return JsonResponse({"error": "Invalid or expired token"}, status=401)

    data = resp.json()

    roles = (
        data.get("resource_access", {})
            .get(CLIENT_ID, {})
            .get("roles", [])
    )

    # 4️⃣ Role check
    if "view_courses" not in roles:
        return JsonResponse(
            {"error": "Forbidden (student role missing)"},
            status=403
        )

    return JsonResponse({
        "message": "Student protected data",
        "user": data.get("preferred_username"),
        "roles": roles
    })