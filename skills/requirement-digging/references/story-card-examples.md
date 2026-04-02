# Story Card Examples

Complete, production-ready story card examples across different domains. Use these 
as templates for quality and format.

---

## Example 1: User Authentication (Chat App)

### Story Card: Phone Registration

```json
{
  "id": "story-001",
  "epic": "User Authentication",
  "title": "User can register with phone number",
  "description": "As a new user, I want to register using my phone number, so that I can create an account and start using the app",
  "acceptanceCriteria": [
    {
      "id": "ac-1",
      "given": "I am on the registration page and have not registered before",
      "when": "I enter a valid 11-digit phone number and tap 'Send Code'",
      "then": "I receive an SMS with a 6-digit verification code",
      "and": "A 60-second countdown timer starts before I can resend"
    },
    {
      "id": "ac-2",
      "given": "I have received the verification code via SMS",
      "when": "I enter the correct 6-digit code and tap 'Verify'",
      "then": "My account is created",
      "and": "I am automatically logged in",
      "and": "I am redirected to the onboarding flow"
    },
    {
      "id": "ac-3",
      "given": "I enter a phone number that is already registered",
      "when": "I tap 'Send Code'",
      "then": "I see an error message: 'This phone number is already registered. Please login instead.'",
      "and": "A 'Go to Login' button is displayed"
    },
    {
      "id": "ac-4",
      "given": "I enter an invalid phone number (not 11 digits)",
      "when": "I tap 'Send Code'",
      "then": "I see an inline error: 'Please enter a valid 11-digit phone number'",
      "and": "No SMS is sent"
    },
    {
      "id": "ac-5",
      "given": "I enter the wrong verification code",
      "when": "I tap 'Verify'",
      "then": "I see an error: 'Invalid code. Please try again.'",
      "and": "I can retry up to 3 times",
      "and": "After 3 failed attempts, I must request a new code"
    }
  ],
  "priority": "Must",
  "estimatedComplexity": "M",
  "dependencies": [],
  "technicalNotes": "Requires SMS provider integration (Aliyun SMS recommended). Store verification code in Redis with 5-minute TTL.",
  "uxNotes": "Show phone number input with country code selector (+86 default). Auto-format as XXX-XXXX-XXXX. Display countdown timer prominently.",
  "sourceRequirement": "func-001"
}
```

### Story Card: Password Login

```json
{
  "id": "story-002",
  "epic": "User Authentication",
  "title": "User can login with phone and password",
  "description": "As a registered user, I want to login with my phone number and password, so that I can access my account securely",
  "acceptanceCriteria": [
    {
      "id": "ac-1",
      "given": "I am on the login page",
      "when": "I enter my registered phone number and correct password",
      "and": "I tap 'Login'",
      "then": "I am authenticated successfully",
      "and": "I am redirected to the home screen",
      "and": "My profile information is loaded"
    },
    {
      "id": "ac-2",
      "given": "I enter an incorrect password",
      "when": "I tap 'Login'",
      "then": "I see an error: 'Incorrect password. Please try again.'",
      "and": "The password field is cleared",
      "and": "I can retry immediately"
    },
    {
      "id": "ac-3",
      "given": "I enter a phone number that is not registered",
      "when": "I tap 'Login'",
      "then": "I see an error: 'This phone number is not registered. Would you like to create an account?'",
      "and": "A 'Register' button is displayed"
    },
    {
      "id": "ac-4",
      "given": "I have failed login 5 times in 15 minutes",
      "when": "I attempt to login again",
      "then": "I see a message: 'Too many failed attempts. Please try again in 30 minutes or reset your password.'",
      "and": "A 'Forgot Password' link is displayed"
    },
    {
      "id": "ac-5",
      "given": "I am on the login page",
      "when": "I tap 'Forgot Password'",
      "then": "I am redirected to the password reset flow"
    }
  ],
  "priority": "Must",
  "estimatedComplexity": "M",
  "dependencies": ["story-001"],
  "technicalNotes": "Implement rate limiting: max 5 attempts per 15 minutes per phone number. Hash passwords with bcrypt (cost=12).",
  "uxNotes": "Show 'Show Password' toggle. Remember phone number for returning users (not password)."
}
```

---

## Example 2: Content Feed (Social App)

### Story Card: View Feed

```json
{
  "id": "story-015",
  "epic": "Content Feed",
  "title": "User can view personalized content feed",
  "description": "As a logged-in user, I want to see a personalized feed of content, so that I can discover interesting posts",
  "acceptanceCriteria": [
    {
      "id": "ac-1",
      "given": "I am logged in and on the home screen",
      "when": "The app loads",
      "then": "I see a feed of posts from users I follow",
      "and": "Posts are sorted by recency (newest first)",
      "and": "Each post shows: author avatar, name, content, timestamp, like count, comment count"
    },
    {
      "id": "ac-2",
      "given": "I am viewing the feed",
      "when": "I scroll down",
      "then": "More posts are loaded automatically (infinite scroll)",
      "and": "A loading spinner appears while fetching more"
    },
    {
      "id": "ac-3",
      "given": "I am viewing the feed",
      "when": "I pull down from the top",
      "then": "The feed refreshes with the latest posts",
      "and": "A 'Refreshing...' indicator is shown"
    },
    {
      "id": "ac-4",
      "given": "There is no internet connection",
      "when": "I open the app",
      "then": "I see cached posts from my last session",
      "and": "I see a banner: 'You're offline. Some content may be outdated.'"
    },
    {
      "id": "ac-5",
      "given": "The feed fails to load (server error)",
      "when": "The app attempts to fetch posts",
      "then": "I see an error screen: 'Couldn't load feed. Tap to retry.'",
      "and": "Tapping anywhere retries the request"
    },
    {
      "id": "ac-6",
      "given": "I am a new user with no followed users",
      "when": "I view the feed for the first time",
      "then": "I see trending/popular posts",
      "and": "I see a suggestion: 'Follow people to see their posts'"
    }
  ],
  "priority": "Must",
  "estimatedComplexity": "L",
  "dependencies": ["story-001", "story-003"],
  "technicalNotes": "Implement pagination: 20 posts per page. Cache last 3 pages locally. Use optimistic UI for scroll.",
  "uxNotes": "Skeleton loader while fetching. Smooth animations for pull-to-refresh. Hide scroll bar for cleaner look."
}
```

### Story Card: Like Post

```json
{
  "id": "story-016",
  "epic": "Content Feed",
  "title": "User can like a post",
  "description": "As a user, I want to like posts I enjoy, so that I can show appreciation and see them later",
  "acceptanceCriteria": [
    {
      "id": "ac-1",
      "given": "I am viewing a post in the feed",
      "when": "I tap the heart/like icon",
      "then": "The icon animates and fills with color",
      "and": "The like count increments by 1 immediately (optimistic update)",
      "and": "The server is notified in the background"
    },
    {
      "id": "ac-2",
      "given": "I have liked a post",
      "when": "I tap the heart/like icon again",
      "then": "The icon returns to outline state",
      "and": "The like count decrements by 1",
      "and": "The server is notified to unlike"
    },
    {
      "id": "ac-3",
      "given": "I like a post but the server request fails",
      "when": "The background sync fails",
      "then": "The UI reverts to the previous state",
      "and": "A subtle error toast appears: 'Couldn't save your like'"
    },
    {
      "id": "ac-4",
      "given": "I am viewing a post",
      "when": "the author deletes the post",
      "then": "The post is removed from my feed",
      "and": "My like is removed from the post's count"
    }
  ],
  "priority": "Must",
  "estimatedComplexity": "S",
  "dependencies": ["story-015"],
  "technicalNotes": "Implement optimistic UI. Queue actions when offline and sync when reconnected. Debounce rapid like/unlike.",
  "uxNotes": "Satisfying animation on like (scale + color fill). Haptic feedback on mobile. Show liked-by-others preview on long-press."
}
```

---

## Example 3: E-commerce (Shopping Cart)

### Story Card: Add to Cart

```json
{
  "id": "story-030",
  "epic": "Shopping Cart",
  "title": "User can add products to shopping cart",
  "description": "As a shopper, I want to add products to my cart, so that I can purchase them later",
  "acceptanceCriteria": [
    {
      "id": "ac-1",
      "given": "I am viewing a product detail page",
      "when": "I select a quantity (default is 1)",
      "and": "I tap 'Add to Cart'",
      "then": "The product is added to my cart",
      "and": "I see a confirmation: 'Added to cart'",
      "and": "The cart icon in the header shows updated item count"
    },
    {
      "id": "ac-2",
      "given": "The product is already in my cart",
      "when": "I add the same product again",
      "then": "The quantity is increased",
      "and": "I see a toast: 'Quantity updated in cart'"
    },
    {
      "id": "ac-3",
      "given": "I try to add more than available stock",
      "when": "I enter quantity > stock",
      "and": "I tap 'Add to Cart'",
      "then": "I see an error: 'Only X items available in stock'",
      "and": "The quantity is adjusted to maximum available"
    },
    {
      "id": "ac-4",
      "given": "I am not logged in",
      "when": "I add a product to cart",
      "then": "The item is stored in local storage",
      "and": "I am prompted to login on checkout",
      "and": "Cart items are merged after login"
    },
    {
      "id": "ac-5",
      "given": "I add a product that goes out of stock",
      "when": "I view my cart later",
      "then": "I see a warning: 'This item is now out of stock'",
      "and": "The item is grayed out and cannot be checked out"
    }
  ],
  "priority": "Must",
  "estimatedComplexity": "M",
  "dependencies": ["story-025"],
  "technicalNotes": "Store cart in Redis for logged-in users, localStorage for guests. Merge on login. Check stock in real-time before checkout.",
  "uxNotes": "Animate cart icon when item added. Show mini-cart preview on desktop. Badge count on cart icon."
}
```

### Story Card: Apply Promo Code

```json
{
  "id": "story-035",
  "epic": "Shopping Cart",
  "title": "User can apply promo code at checkout",
  "description": "As a shopper, I want to apply a promo code, so that I can get a discount on my order",
  "acceptanceCriteria": [
    {
      "id": "ac-1",
      "given": "I am on the checkout page",
      "when": "I enter a valid promo code",
      "and": "I tap 'Apply'",
      "then": "The discount is applied to my order total",
      "and": "I see the discount amount and new total",
      "and": "The promo code is locked and cannot be changed"
    },
    {
      "id": "ac-2",
      "given": "I enter an invalid promo code",
      "when": "I tap 'Apply'",
      "then": "I see an error: 'Invalid promo code. Please check and try again.'",
      "and": "The order total remains unchanged"
    },
    {
      "id": "ac-3",
      "given": "I enter an expired promo code",
      "when": "I tap 'Apply'",
      "then": "I see an error: 'This promo code has expired'",
      "and": "The expiry date is displayed"
    },
    {
      "id": "ac-4",
      "given": "My cart total is $50",
      "when": "I try to apply a code that requires $100 minimum",
      "then": "I see an error: 'Minimum order of $100 required for this promo'",
      "and": "I see how much more I need to add"
    },
    {
      "id": "ac-5",
      "given": "I have applied a promo code",
      "when": "I remove items from cart bringing total below minimum",
      "then": "I see a warning: 'Your order no longer meets the minimum for this promo'",
      "and": "The promo is removed",
      "and": "The total is recalculated"
    },
    {
      "id": "ac-6",
      "given": "I have applied a promo code",
      "when": "I tap 'Remove' next to the applied code",
      "then": "The promo is removed",
      "and": "The total is recalculated",
      "and": "I can enter a different code"
    }
  ],
  "priority": "Should",
  "estimatedComplexity": "M",
  "dependencies": ["story-030", "story-032"],
  "technicalNotes": "Validate promo codes server-side. Check: validity period, minimum order, applicable products, usage limit per user.",
  "uxNotes": "Show promo code field prominently. Auto-format code input (uppercase, spaces). Show savings amount in green."
}
```

---

## Quality Comparison

### Good vs Bad Acceptance Criteria

| Good ✅ | Bad ❌ | Why |
|---------|-------|-----|
| "Given invalid email, When submit, Then show error 'Please enter valid email'" | "Form should validate properly" | Specific vs vague |
| "Given cart total < $100, When apply promo, Then show minimum error" | "Promo should work correctly" | Testable vs untestable |
| "Given no internet, When open app, Then show cached posts + offline banner" | "App should handle offline" | Complete scenario vs hand-wavy |
| "After 3 failed attempts, lock account for 30 minutes" | "Prevent brute force attacks" | Measurable vs abstract |

---

## Template for New Story Cards

```json
{
  "id": "story-XXX",
  "epic": "Epic Name",
  "title": "User can [action]",
  "description": "As a [role], I want [feature], so that [value]",
  "acceptanceCriteria": [
    {
      "id": "ac-1",
      "given": "[precondition]",
      "when": "[action]",
      "then": "[result]",
      "and": "[additional result if needed]"
    }
  ],
  "priority": "Must|Should|Could",
  "estimatedComplexity": "S|M|L|XL",
  "dependencies": ["story-XXX"],
  "technicalNotes": "",
  "uxNotes": "",
  "sourceRequirement": "func-XXX"
}
```

Use these examples as quality benchmarks. Every story card you create should 
be this detailed and testable.
