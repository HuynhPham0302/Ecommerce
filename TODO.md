# Project TODO

## Application Hardening
- [ ] Enforce JWT authentication on non-auth routes by adding a reusable token verification decorator across blueprints (`app/api/*.py`).
- [ ] Standardize all responses to use `APIResponse` for consistency (`app/api/users.py`, `app/api/orders.py`, etc.).
- [ ] Introduce payload validation (Marshmallow, Pydantic, or manual schemas) for every POST/PUT endpoint to return helpful 400 errors instead of generic exceptions.
- [ ] Add missing update and delete routes for each resource to provide full CRUD coverage (addresses, categories, products, orders, order items, payments, users).
- [ ] Implement pagination, filtering, and search on list endpoints (products, orders) to support realistic storefront workloads.

## Bug Fixes
- [ ] Convert incoming status strings to `OrderStatus` and `PaymentStatus` enums before persisting (`app/api/orders.py`, `app/api/payments.py`).
- [ ] Default optional fields using `.get()` to avoid KeyErrors in `create_address`, `register`, and similar handlers.
- [ ] Correct typo in the orders error response (`errpr_code`) and audit other response fields for accuracy.
- [ ] Add an explicit `__tablename__ = "order_items"` to `OrderItem` so the ORM schema matches `schema.sql` and the seed data.
- [ ] Ensure `order_date` and `payment_date` fields fall back to `datetime.utcnow()` when the client omits them and parse ISO strings when provided.
- [ ] Validate SKU uniqueness (instead of name-only checks) when creating products.

## Data & Storage
- [ ] Integrate Flask-Migrate (Alembic) for repeatable schema migrations.
- [ ] Reconcile differences between `schema.sql` and SQLAlchemy models (naming conventions, constraints, indexes).
- [ ] Add seed data idempotency guards or a `--drop` flag so developers can choose whether to wipe tables.

## Security
- [ ] Store hashed refresh tokens or a token blacklist to support logout/expiration workflows.
- [ ] Rate-limit authentication endpoints and add brute-force protection.
- [ ] Move secrets out of the committed `.env` file and document secure handling practices.

## Testing & Quality
- [ ] Set up pytest with an app factory fixture and an in-memory SQLite database for fast tests.
- [ ] Cover auth flows, happy-path CRUD, and error cases with integration tests.
- [ ] Add linting/formatting (ruff, black, isort) and wire them into CI.

## Developer Experience
- [ ] Provide Docker/Docker Compose definitions for the API and MySQL development database.
- [ ] Add Makefile targets for linting, testing, and formatting.
- [ ] Publish a Postman/Thunder Client collection or OpenAPI JSON export for easy onboarding.

## Documentation
- [ ] Extend README with endpoint examples that include auth headers once protection is in place.
- [ ] Document environment variable options (e.g., alternate DATABASE_URLs, JWT expiry overrides).
- [ ] Write a short CONTRIBUTING guide covering branching, testing, and review expectations.
