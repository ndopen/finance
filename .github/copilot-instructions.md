# Copilot Instructions

This is a full-stack FastAPI + React template for building modern web applications with auto-generated type-safe clients.

## Architecture Overview

**Backend (FastAPI)**: Python API with SQLModel ORM, PostgreSQL database, JWT authentication, and auto-generated OpenAPI specs.
**Frontend (React)**: TypeScript SPA using TanStack Router/Query, Chakra UI, and auto-generated API client from OpenAPI.
**Development**: Docker Compose with hot-reload, shared .env configuration, and integrated testing.

### Key Integration Points

- **API Client Generation**: Run `./scripts/generate-client.sh` after backend schema changes to update `frontend/src/client/`
- **Authentication Flow**: JWT tokens managed by `useAuth` hook, with `CurrentUser` dependency injection on backend
- **Database**: SQLModel handles both Pydantic models and SQLAlchemy tables in single class definitions
- **CORS**: Backend auto-configures CORS for frontend URL from `FRONTEND_HOST` environment variable

## Development Workflows

### Starting Development
```bash
# Full stack with hot-reload
docker compose watch

# Individual services (after stopping Docker service)
docker compose stop backend
cd backend && uvicorn app.main:app --reload

docker compose stop frontend  
cd frontend && npm run dev
```

### Common Tasks
```bash
# Regenerate frontend API client (after backend changes)
./scripts/generate-client.sh

# Run tests
./scripts/test-local.sh                    # Full stack tests
cd backend && python -m pytest            # Backend only
cd frontend && npm run playwright test     # E2E tests

# Database migrations
cd backend && alembic revision --autogenerate -m "description"
cd backend && alembic upgrade head

# Linting
cd backend && ruff check --fix            # Python (Ruff)
cd frontend && npm run lint               # TypeScript (Biome)
```

## Test-Driven Development (TDD) Rules

Follow TDD principles for robust, maintainable code. Write tests first, then implement functionality.

### TDD Workflow

1. **Red**: Write a failing test that describes the desired functionality
2. **Green**: Write the minimum code needed to make the test pass
3. **Refactor**: Improve code quality while keeping tests green

### Backend TDD Patterns

**API Endpoint Development**:
```python
# 1. First, write the test (Red)
def test_create_item_success(client: TestClient, normal_user_token_headers: dict):
    data = {"title": "Test Item", "description": "Test description"}
    response = client.post("/api/v1/items/", headers=normal_user_token_headers, json=data)
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == data["title"]
    assert "id" in content

# 2. Then implement the endpoint (Green)
@router.post("/", response_model=ItemPublic)
def create_item(
    session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Item:
    item = Item.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
```

**Model Validation Tests**:
```python
# Test model constraints before implementation
def test_item_title_required():
    with pytest.raises(ValidationError):
        ItemCreate(description="No title")

def test_item_title_max_length():
    with pytest.raises(ValidationError):
        ItemCreate(title="x" * 256, description="Too long")
```

**CRUD Operation Tests**:
```python
# Test complete CRUD operations
def test_item_crud_operations(session: Session, user: User):
    # Create
    item = create_item(session, ItemCreate(title="Test"), user.id)
    assert item.title == "Test"
    
    # Read
    stored_item = get_item(session, item.id)
    assert stored_item.id == item.id
    
    # Update
    updated = update_item(session, item.id, ItemUpdate(title="Updated"))
    assert updated.title == "Updated"
    
    # Delete
    delete_item(session, item.id)
    assert get_item(session, item.id) is None
```

### Frontend TDD Patterns

**Component Testing**:
```tsx
// 1. Write component test first (Red)
describe('ItemForm', () => {
  it('submits form data correctly', async () => {
    const mockSubmit = vi.fn()
    render(<ItemForm onSubmit={mockSubmit} />)
    
    await user.type(screen.getByLabelText(/title/i), 'Test Item')
    await user.click(screen.getByRole('button', { name: /submit/i }))
    
    expect(mockSubmit).toHaveBeenCalledWith({ title: 'Test Item' })
  })
})

// 2. Then implement component (Green)
const ItemForm = ({ onSubmit }: { onSubmit: (data: ItemCreate) => void }) => {
  const { register, handleSubmit } = useForm<ItemCreate>()
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input {...register('title')} aria-label="Title" />
      <Button type="submit">Submit</Button>
    </form>
  )
}
```

**Hook Testing**:
```tsx
// Test custom hooks behavior
describe('useItems', () => {
  it('fetches items on mount', async () => {
    const { result } = renderHook(() => useItems(), {
      wrapper: QueryClientProvider,
    })
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })
    
    expect(result.current.data).toHaveLength(2)
  })
})
```

### E2E TDD Approach

**User Journey Tests**:
```typescript
// Define user stories as tests first
test('user can create and manage items', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[data-testid=email]', 'user@example.com')
  await page.fill('[data-testid=password]', 'password')
  await page.click('[data-testid=login]')
  
  // Create item
  await page.click('[data-testid=create-item]')
  await page.fill('[data-testid=item-title]', 'My Item')
  await page.click('[data-testid=save]')
  
  // Verify item appears
  await expect(page.locator('text=My Item')).toBeVisible()
})
```

### TDD Best Practices

**Test Organization**:
- Group related tests in describe blocks
- Use descriptive test names that explain expected behavior
- Follow AAA pattern: Arrange, Act, Assert
- Keep tests independent and isolated

**Test Data Management**:
```python
# Use factories for consistent test data
@pytest.fixture
def sample_item_data():
    return {
        "title": "Sample Item",
        "description": "Sample description",
    }

# Clean database state between tests
@pytest.fixture(autoscope="function")
def db_session():
    # Setup clean database state
    yield session
    # Cleanup after test
```

**Mocking Strategy**:
- Mock external dependencies (APIs, databases in unit tests)
- Use real implementations in integration tests
- Mock time-dependent or random behavior for consistent tests

**Test Coverage Goals**:
- Aim for 90%+ coverage on business logic
- Focus on edge cases and error conditions
- Test both happy path and failure scenarios

### Running Tests in TDD Cycle

```bash
# Backend: Run specific test during development
cd backend && python -m pytest tests/api/routes/test_items.py::test_create_item -v

# Frontend: Run tests in watch mode
cd frontend && npm run test:watch

# Quick feedback loop
./scripts/test-local.sh --fast  # Skip slower integration tests during development
```

## Code Patterns & Conventions

### Backend (FastAPI + SQLModel)

**Model Pattern**: SQLModel combines Pydantic and SQLAlchemy - use single classes for API and DB:
```python
# app/models.py
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)

class Item(ItemBase, table=True):  # Database table
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id")

class ItemPublic(ItemBase):  # API response
    id: uuid.UUID
```

**Dependency Injection**: Use these standard deps in route functions:
```python
# app/api/routes/
def create_item(
    session: SessionDep,        # Database session
    current_user: CurrentUser,  # Authenticated user
    item_in: ItemCreate,       # Request body
) -> ItemPublic:
```

**Route Organization**: Group by resource in `app/api/routes/`, include in `app/api/main.py`:
```python
# New route file: app/api/routes/items.py
router = APIRouter(prefix="/items", tags=["items"])

# Register in app/api/main.py
from app.api.routes import items
api_router.include_router(items.router)
```

### Frontend (React + TypeScript)

**Authentication**: Use `useAuth` hook for all auth operations:
```tsx
import useAuth from "@/hooks/useAuth"

const { user, logout, loginMutation, signUpMutation } = useAuth()
const isAuthenticated = !!user
```

**API Calls**: Use auto-generated client with TanStack Query:
```tsx
import { ItemsService } from "@/client"
import { useQuery, useMutation } from "@tanstack/react-query"

// Query
const { data: items } = useQuery({
  queryKey: ["items"],
  queryFn: () => ItemsService.readItems({}),
})

// Mutation  
const createMutation = useMutation({
  mutationFn: ItemsService.createItem,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ["items"] }),
})
```

**Routing**: Use TanStack Router file-based routing in `src/routes/`:
```tsx
// src/routes/items.tsx
export const Route = createFileRoute("/items")({
  component: ItemsPage,
  beforeLoad: ({ context }) => {
    if (!context.auth.user) throw redirect({ to: "/login" })
  },
})
```

**Forms**: Use react-hook-form with Chakra UI components:
```tsx
import { useForm } from "react-hook-form"

const { register, handleSubmit, formState: { errors } } = useForm<ItemCreate>()
```

### Configuration

**Environment**: Backend reads from `../.env` (project root), frontend from `.env.local`:
- `SECRET_KEY`: JWT signing (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- `POSTGRES_PASSWORD`: Database password
- `FRONTEND_HOST`: Frontend URL for CORS (default: http://localhost:5173)

**Database**: Postgres connection auto-configured, migrations in `backend/alembic/versions/`

## File Structure Conventions

- **Backend Routes**: `app/api/routes/{resource}.py` - one file per resource
- **Models**: `app/models.py` - all SQLModel classes (keep together for relationships)
- **Frontend Components**: `src/components/{Feature}/` - group by feature area
- **Generated Client**: `src/client/` - never edit manually, regenerated from OpenAPI
- **Routing**: `src/routes/` - file-based routing matches URL structure

## Testing

- **Backend**: Pytest with fixtures in `backend/tests/conftest.py`
- **Frontend**: Playwright E2E tests in `frontend/tests/`
- **Full Stack**: `./scripts/test-local.sh` runs both backend tests and frontend E2E

## Troubleshooting

- **Client sync issues**: Run `./scripts/generate-client.sh` after backend model changes
- **CORS errors**: Check `FRONTEND_HOST` in .env matches your frontend URL
- **Database issues**: Check logs with `docker compose logs db` or reset with `docker compose down -v`
- **Hot reload not working**: Use `docker compose watch` instead of `docker compose up`
