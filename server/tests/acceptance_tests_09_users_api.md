# Users API - Acceptance Tests (Plain English)

## Goal
Read-only Users endpoints separate from auth flows.

## Scenarios

1) List users (defaults)
- When I GET `/api/v1/users`
- Then I receive 200 OK
- And the body has `users` (array) and `total` (number)

2) List users with pagination
- When I GET `/api/v1/users?skip=1&limit=2`
- Then I receive 200 OK
- And the array length is <= 2

3) Get user by numeric id
- Given a user exists with id N
- When I GET `/api/v1/users/N`
- Then I receive 200 OK and the user has `id == N`
- When I GET `/api/v1/users/999999`
- Then I receive 404 Not Found

4) Get user by public_id
- Given a user exists with `public_id = U`
- When I GET `/api/v1/users/public/U`
- Then I receive 200 OK and the user has `public_id == U`
- When I GET `/api/v1/users/public/non-existent`
- Then I receive 404 Not Found

5) Search users
- When I GET `/api/v1/users/search/?q=joe`
- Then I receive 200 OK
- And `users` contains only users whose name or email match `joe` (case-insensitive)

6) Response shape
- Each user has: `id, public_id, email, first_name, last_name, phone, roles, is_active, is_verified, personalization, last_login, created_at, updated_at`


