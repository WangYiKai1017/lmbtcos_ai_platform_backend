# 5W1H Questioning Framework

A comprehensive question bank for requirement elicitation. Use these questions 
to guide dialogue and uncover hidden requirements.

---

## WHAT - Feature & Function Discovery

### Core Features

| Question | Purpose | Follow-up |
|----------|---------|-----------|
| "What specific features do you envision?" | Open discovery | "Can you give me an example?" |
| "What should the user see when they first open the app?" | Entry point | "What's the most important thing on that screen?" |
| "What actions can the user take?" | Action mapping | "What happens after they do that?" |
| "What data needs to be displayed?" | Data requirements | "Where does this data come from?" |
| "What data needs to be collected from users?" | Input requirements | "Is this required or optional?" |
| "What should happen if something goes wrong?" | Error handling | "What kind of errors do you anticipate?" |

### Feature Prioritization

| Question | Purpose |
|----------|---------|
| "What are the absolute must-have features for launch?" |
| "What features would be nice to have but aren't critical?" |
| "If you could only have 3 features, what would they be?" |
| "What feature would make this truly unique?" |

### Content & Media

| Question | Purpose |
|----------|---------|
| "What type of content will users interact with?" |
| "Will users upload images/videos/documents?" |
| "What file formats need to be supported?" |
| "Are there size limits for uploads?" |
| "Does content need to be moderated before publishing?" |

---

## WHO - User & Stakeholder Discovery

### Primary Users

| Question | Purpose | Follow-up |
|----------|---------|-----------|
| "Who is the primary user of this system?" | User identification | "Can you describe a typical user?" |
| "What is their age range?" | Demographics | |
| "What is their technical proficiency level?" | UX calibration | "Should we optimize for beginners or power users?" |
| "How often will they use this?" | Usage frequency | "Daily? Weekly? Occasionally?" |
| "What device will they primarily use?" | Platform decision | "Mobile, desktop, or both?" |

### User Roles

| Question | Purpose |
|----------|---------|
| "Are there different types of users (roles)?" |
| "What can admins do that regular users can't?" |
| "Do users need different permission levels?" |
| "Will there be guest users (unauthenticated)?" |
| "What actions are restricted to certain roles?" |

### Stakeholders

| Question | Purpose |
|----------|---------|
| "Who else has a stake in this project?" |
| "Who needs to approve the final product?" |
| "Are there regulatory/compliance stakeholders?" |
| "Who will maintain this after launch?" |

---

## WHEN - Timing & Scenario Discovery

### Usage Scenarios

| Question | Purpose | Follow-up |
|----------|---------|-----------|
| "When will users typically use this?" | Context discovery | "What triggers them to open the app?" |
| "Is this for work or personal use?" | Context | |
| "Will users be in a hurry when using this?" | UX implication | "Should we optimize for speed?" |
| "Will they use it while multitasking?" | Attention level | |

### Time-Sensitive Features

| Question | Purpose |
|----------|---------|
| "Are there any time-limited features (promotions, deadlines)?" |
| "Does data expire or need archival?" |
| "Should the system send time-based notifications?" |
| "Are there peak usage times we should plan for?" |

### Project Timeline

| Question | Purpose |
|----------|---------|
| "When do you need this launched?" |
| "Are there milestones or phases?" |
| "What happens if we miss the deadline?" |
| "Is there a specific event this is tied to?" |

---

## WHERE - Platform & Deployment Discovery

### Platform

| Question | Purpose | Follow-up |
|----------|---------|-----------|
| "Where will users access this?" | Platform | "Web, iOS, Android, desktop app?" |
| "Do you need responsive design for mobile?" | Mobile strategy | |
| "Should it work offline?" | Offline capability | "What features should work without internet?" |
| "Do you need a progressive web app (PWA)?" | PWA consideration | |

### Deployment

| Question | Purpose |
|----------|---------|
| "Where will this be hosted?" |
| "Cloud (which provider?) or on-premise?" |
| "Are there geographic restrictions (GDPR, data sovereignty)?" |
| "Do you need multi-region deployment?" |

### Integration Points

| Question | Purpose |
|----------|---------|
| "Where does this fit in your existing systems?" |
| "What other systems does this need to integrate with?" |
| "Are there existing APIs we should use?" |
| "Do we need to provide APIs for others to consume?" |

---

## WHY - Value & Motivation Discovery

### Business Value

| Question | Purpose | Follow-up |
|----------|---------|-----------|
| "Why is this project important?" | Business goal | "What does success look like?" |
| "What problem does this solve?" | Problem statement | "How are users solving this now?" |
| "Why now? What's the urgency?" | Timing | |
| "Why this approach vs alternatives?" | Strategy | "What alternatives did you consider?" |

### User Value

| Question | Purpose |
|----------|---------|
| "Why would users choose this over competitors?" |
| "Why is this feature valuable to users?" |
| "Why would users recommend this to others?" |

### Success Metrics

| Question | Purpose |
|----------|---------|
| "How will you measure success?" |
| "What KPIs matter most?" |
| "What would make you say 'this was worth it'?" |
| "What's the ROI expectation?" |

---

## HOW - Implementation & Interaction Discovery

### User Interaction

| Question | Purpose | Follow-up |
|----------|---------|-----------|
| "How do you imagine users interacting with this?" | Interaction model | "Touch, keyboard, voice?" |
| "How should the system respond to errors?" | Error UX | "Show message? Auto-retry? Escalate?" |
| "How will users get help if they're stuck?" | Support | "In-app help? Chatbot? Documentation?" |
| "How should notifications be delivered?" | Notification | "Email, SMS, push, in-app?" |

### Technical Expectations

| Question | Purpose |
|----------|---------|
| "How many concurrent users do you expect?" |
| "How much data will be stored?" |
| "How fast should pages load?" |
| "How will you handle user support?" |

### Process & Workflow

| Question | Purpose |
|----------|---------|
| "How does a user complete [key workflow]?" |
| "How should approvals/reviews work?" |
| "How will content be moderated?" |
| "How should data be exported/backed up?" |

---

## Probing Techniques

### The "Five Whys"

When user states a requirement, ask "why" iteratively:

```
User: "I need a search feature"
→ Why? "So users can find products"
→ Why is that hard? "Because we have 10,000+ products"
→ Why can't they browse? "Categories are too deep"
→ Why not fix categories? "Search is faster"
→ Root need: Quick product discovery (search is one solution)
```

### The "Concrete Example" Request

When user is abstract:

```
User: "It should be user-friendly"
→ "Can you give me an example of an app you think is user-friendly?"
→ "What specifically about that app feels user-friendly?"
```

### The "Edge Case" Probe

```
User: "Users can upload photos"
→ "What if someone tries to upload a 100MB file?"
→ "What if the upload fails halfway?"
→ "What if someone uploads inappropriate content?"
```

### The "Comparison" Anchor

```
User: "I want a social feed"
→ "Are you thinking more like WeChat Moments or like Twitter?"
→ "What do you like about [example] that you want to emulate?"
```

### The "Negative" Question

```
"What should the system NOT do?"
"What features are explicitly out of scope?"
"What would make users delete this app immediately?"
```

---

## Question Sequencing Strategy

### Opening Phase (Turns 1-3)
- Start broad: "Tell me about..."
- Establish context: Who, what, why
- Build rapport: Show understanding

### Deep Dive Phase (Turns 4-12)
- Focus on one area per turn
- Follow up on ambiguities
- Request examples
- Challenge assumptions gently

### Wrapping Up Phase (Turns 13+)
- Summarize understanding
- Confirm no major gaps
- Ask "anything else important?"
- Set expectations for next steps

---

## Common Vague Statements & How to Probe

| Vague Statement | Probe Question |
|-----------------|----------------|
| "It should be fast" | "What's an acceptable load time? Under 1 second? 3 seconds?" |
| "User-friendly interface" | "Can you name an app you consider user-friendly? What makes it so?" |
| "Secure authentication" | "Do you need 2FA? Password requirements? Social login?" |
| "Modern design" | "What does 'modern' mean to you? Minimalist? Colorful? Material Design?" |
| "Handle lots of users" | "What's your expected concurrent user count? 100? 10,000? 1M?" |
| "Integrate with our systems" | "Which specific systems? Do they have APIs?" |
| "Mobile responsive" | "Should it work on tablets? Small phones? Landscape mode?" |

---

## Red Flags to Watch For

| Red Flag | What It Means | Follow-up |
|----------|---------------|-----------|
| User says "just like X" | May not understand complexity | "What specifically about X do you want?" |
| User says "it's simple" | May underestimate scope | "Walk me through the steps" |
| User says "we'll figure it out later" | Critical decision deferred | "This affects architecture - can we decide now?" |
| User contradicts themselves | Unclear requirements | "Earlier you said X, now you're saying Y - which is correct?" |
| User can't give examples | Haven't thought it through | "Let's sketch out a sample scenario" |

---

Use this framework to guide your questioning, but stay flexible and follow 
the user's energy. The goal is understanding, not checking boxes.
