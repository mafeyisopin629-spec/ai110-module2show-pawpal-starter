# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- I designed PawPal+ using four main classes: Owner, Pet, Task, and Scheduler. The Owner class is responsible for storing the owner’s information and managing their pets. The Pet class represents each pet and stores details such as name, species, age, and its list of tasks. The Task class represents individual care activities like feeding, walking, medication, or appointments, and includes details such as time, duration, priority, and completion status. The Scheduler class is responsible for organizing tasks, sorting them, detecting conflicts, and generating a daily schedule.


- These classes reflect real-world relationships in a pet care system. An owner can have multiple pets, each pet can have multiple tasks, and the scheduler works with tasks to create an organized daily plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Answer
I made a few small design changes after reviewing my class skeleton. I added explicit relationships by linking each Task to a Pet and each Pet to an Owner so the connections in the system would be clearer. I also changed task priority to use an enum instead of a plain value so priority levels would be more organized and easier to manage later in the implementation.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Answer
One tradeoff in my scheduler is that I prioritized readability over advanced optimization in my conflict detection algorithm. I used a simple approach that compares adjacent tasks after sorting them by time. This makes the logic easy to understand and maintain, but it may not handle more complex scheduling scenarios beyond basic overlaps. 

I chose this design because it fits the current scale of the application and keeps the code clear and beginner-friendly.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?


---

## 5. Reflection

Reflect on AI Strategy: Specifically describe your experience with VS Code Copilot:

- Which Copilot features were most effective for building your scheduler?
- Give one example of an AI suggestion you rejected or modified to keep your system design clean.
- How did using separate chat sessions for different phases help you stay organized?

Answer

- Using VS Code Copilot and AI tools was very helpful in building my scheduler system. The most effective feature for me was using AI to generate code structure and logic for methods like sorting tasks, filtering, and detecting conflicts. It helped me move faster and understand how to implement certain ideas, especially with things like using sorted() with a lambda function and handling recurring tasks with timedelta.

- One example of an AI suggestion I modified was the conflict detection logic. The AI suggested a more complex approach comparing many task combinations, but I simplified it to only compare adjacent tasks after sorting. This made the code easier to read and still efficient, while maintaining correct functionality.

- Using separate chat sessions for different phases helped me stay organized. I was able to focus on one part of the project at a time (like backend logic, testing, or UI) without mixing everything together. This made it easier to debug and understand what I was working on at each stage.

Summarize what you learned about being the "lead architect" when collaborating with powerful AI tools.

Answer
Throughout this project, I learned that even when using AI tools, I still needed to act as the “lead architect.” The AI helped generate ideas and code, but I had to decide what made sense for my design and make sure everything worked together properly.

I had to review, adjust, and sometimes simplify the AI-generated solutions to keep my system clean and understandable. This experience showed me that AI is a powerful assistant, but the responsibility for designing and organizing the system still depends on me as the developer.

Overall, this project helped me understand how to combine my own thinking with AI assistance to build a complete, working system.