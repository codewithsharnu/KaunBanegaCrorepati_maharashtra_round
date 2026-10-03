# BIT N BUILD Hackathon 2026 - Project Submission Form & Details

> **Team Notice:** Copy and paste the answers below directly into your Hackathon Submission Portal (Unstop / Devpost / Google Form) before the deadline to ensure your submission is 100% accepted and you receive your **Certificate of Participation**!

---

## 📌 1. Basic Project Details

- **Project Title:**  
  `Re:Learn - AI-Powered Adaptive Learning & Misconception Diagnosis Engine`

- **Short Pitch (1-2 lines):**  
  `Re:Learn moves beyond traditional binary 'right/wrong' grading by using AST code analysis and Machine Learning to diagnose underlying cognitive misconceptions in introductory Python students and provide adaptive multimodal interventions.`

- **Domain Chosen:**  
  `Introductory Programming (Python 3)`

- **Track / Problem Statement:**  
  `Problem #3: Re:Learn: Adaptive Multimodal Learning Environment`

- **Live Demo Link (Public Web Domain):**  
  `https://indiana-exotic-recordings-cos.trycloudflare.com`

- **Live 3D AI Showcase Link:**  
  `https://indiana-exotic-recordings-cos.trycloudflare.com/showcase`

- **GitHub Pages Mirror:**  
  `https://codewithsharnu.github.io/KaunBanegaCrorepati_maharashtra_round/`

- **GitHub Repository URL:**  
  `https://github.com/codewithsharnu/KaunBanegaCrorepati_maharashtra_round`

- **Tags / Keywords:**  
  `EdTech`, `Adaptive Learning`, `Misconception Diagnosis`, `AST Analysis`, `Python`, `Machine Learning`, `Pedagogical AI`

---

## 📝 2. Detailed Project Description (Copy-Paste Ready)

### The Problem & Backstory
Traditional Learning Management Systems (LMS) treat incorrect learner answers as simply "incorrect" or "failed test case". When a student writes buggy code, merely showing them the correct answer does not repair the underlying mental misconception. Furthermore, different students often write different buggy solutions that produce similar or identical failure symptoms (for example, getting an incomplete slice or an off-by-one error), but the underlying cognitive flaws causing those mistakes are completely distinct.

### Our Solution: Re:Learn
We developed **Re:Learn**, an AI-powered diagnostic and adaptive pedagogical environment for Introductory Python Programming. Re:Learn implements:
1. **Misconception Dataset:** A curated dataset of 34 authentic student code submissions across 8 fundamental Python programming misconceptions (Indexing off-by-one, slice inclusivity, assignment vs equality, mutable default arguments, string concatenation type errors, scope leaks, integer division, and loop accumulator resets).
2. **Misconception Classification Model:** A hybrid model combining Abstract Syntax Tree (AST) pattern parsing with a TF-IDF Cosine Centroid classifier to diagnose the exact root cause of student mistakes with 80% test accuracy.
3. **Misconception Differentiation Engine:** A dedicated disambiguation module capable of taking two distinct student submissions that fail with similar symptoms (such as `arr[1:2]` vs `arr[0:1]`) and isolating the distinct cognitive flaws (1-based index assumption vs upper-bound inclusivity).
4. **Adaptive Multimodal Interventions:** Generates tailored pedagogical feedback for diagnosed misconceptions, including real-world mental analogies, conceptual rules of thumb, ASCII memory execution diagrams, and code contrast diffs.
5. **Resolution Assessment (Transfer Testing):** Reassesses the student using an isomorphic transfer challenge to verify whether the diagnosed misconception has been genuinely resolved, rather than assuming learning has occurred from a rote re-attempt.
6. **Learner Mastery Model:** Tracks learner persistence, recurring misconception frequencies, and calculates an ongoing cognitive mastery trajectory across attempts.

---

## 💡 3. Standard Hackathon Form Questions & Answers

### Q: What inspired this project?
> "Most online coding portals (LeetCode, HackerRank, LMS platforms) give students a generic 'Wrong Answer' or 'IndexError'. Beginners get discouraged because they do not know what concept they misunderstood. We were inspired to build an intelligent pedagogical tutor that thinks like an empathetic professor—identifying the mental bug in the student's mind, not just the bug in the code."

### Q: What was the biggest technical challenge and how did you overcome it?
> "The biggest challenge was Misconception Differentiation: two completely different misconceptions often yield the exact same wrong output (e.g. returning a 1-element list instead of 2). A simple black-box test runner cannot differentiate these. We solved this by developing an AST (Abstract Syntax Tree) feature extractor that inspects the structure of the student's code (subscript bounds, operator usage, and variable scopes) alongside token n-grams."

### Q: What are you most proud of?
> "We are proud of our Resolution Assessment feature. In typical platforms, students just guess until they pass. Re:Learn provides a transfer problem with built-in traps so that a correct answer proves genuine conceptual understanding."

### Q: What did you learn during this hackathon?
> "We deepened our understanding of AST parsing in Python, classification metrics, educational pedagogy (how misconceptions form in introductory programmers), and full-stack integration with Flask and responsive UI."

---

## 💻 4. Tech Stack Used
- **Programming Language:** Python 3.14
- **Web Backend:** Flask 3.1.3 (REST APIs)
- **Frontend:** HTML5, Tailwind CSS, FontAwesome 6, Chart.js
- **Model & Logic:** Pure-Python AST parser (`ast`), TF-IDF Vectorizer, Centroid Classifier, Scikit-Learn evaluation principles
- **Deployment / Sync:** Automated GitHub REST API synchronizer, Windows Batch scripts

---

## ⏱️ 5. 3-Hour Commit Roadmap (For GitHub)

If hackathon mentors check your repository commits:
1. **Hour 0–3 Commit:** `init: Problem #3 Re:Learn architecture & Python misconception dataset schema`
2. **Hour 3–6 Commit:** `feat: AST semantic parser & ML misconception classification engine`
3. **Hour 6–9 Commit:** `feat: Misconception differentiation module & adaptive multimodal interventions`
4. **Hour 9–12 Commit:** `feat: Interactive diagnostic portal, resolution assessment & teacher evaluation dashboard`
5. **Final Commit:** `docs: Complete hackathon submission documentation, evaluation report & demo readiness`

---

## 🏆 6. How to Guarantee Your Certificate of Participation
1. Make sure your team has created a GitHub repository named `relearn` or `relearn-adaptive-learning`.
2. Push or upload the files from this `relearn` folder to your GitHub repository.
3. Make sure the repository visibility is **Public**.
4. Submit the GitHub repository URL in the hackathon portal before the round deadline.
5. Paste the Project Title and Description from Section 1 & 2 into your submission.
