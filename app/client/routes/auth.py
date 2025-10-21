from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

client_auth_bp = Blueprint("client_auth", __name__)

@client_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    email = ""

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            error = "Email and password are required."
        else:
            # Call the public API to authenticate instead of hitting the database directly.
            with current_app.test_client() as client:
                api_response = client.post(
                    "/api/auth/login",
                    json={"email": email, "password": password},
                )

            payload = api_response.get_json(silent=True) or {}

            if api_response.status_code != 200 or not payload.get("success"):
                error = payload.get("message", "Invalid email or password.")
            else:
                data = payload.get("data", {})
                user = data.get("user") or {}
                token = data.get("token")

                session["user_id"] = user.get("id")
                session["user_role"] = user.get("role")
                session["user_email"] = user.get("email")
                session["auth_token"] = token

                flash("Login successful.", "success")
                return redirect(url_for("client_auth.login"))

    return render_template("login.html", error=error, email=email)
