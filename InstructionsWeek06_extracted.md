# Week 06 Instructions - Code Evaluation Criteria

## 1. Correctness (Logic, Bugs, and Security)

**Definition:** Does the generated code work as intended free of bugs, and without introducing security vulnerabilities?

**What to check:**
- Produces correct results for normal and edge cases
- No logic errors / broken functionality / regressions
- Safe error handling (null checks, input validation)
- No security flaws (e.g., SQL injection, unsafe APIs, hard-coded secrets)


1 — Code is broken or introduces severe security vulnerabilities.
2 — Runs but has obvious errors or security concerns.
3 — Mostly correct but with a significant bug or weak security practice.
4 — Minor oversight (e.g., one missed edge case) but otherwise correct and safe.
5 — Fully correct and secure: no bugs or unsafe patterns.

**Score:** ___
**Notes:** _______________

## 2. Completeness (Fully Satisfies the Request)

**Definition:** Does the code fully implement the user's request?

**What to check:**
- All requested features, fixes, or requirements implemented
- All input/output requirements and constraints covered
- Nothing left partially done or skipped

1 — Barely addresses the request or solves the wrong problem.
2 — Major parts of the request are unaddressed.
3 — Only partially satisfies the request; significant pieces are missing.
4 — Almost complete, with one small omission or missed nuance.
5 — Fully implements all requested requirements.


**Score:** ___
**Notes:** _______________

## 3. Minimality (No Unnecessary Changes)

**Definition:** Does the change focus only on what's needed, without touching unrelated code or adding extraneous changes?

**What to check:**
- Avoids unrelated refactoring, formatting, or renaming
- No unnecessary files, dependencies, or helpers added
- Diff is minimal and easy to review

1 — Diff is sprawling or introduces unrelated modifications.
2 — Many irrelevant or noisy changes.
3 — Several unrelated edits that reduce reviewability.
4 — Small unnecessary edits (e.g., formatting) but not distracting.
5 — Purely minimal; only relevant line/files are changed.


**Score:** ___
**Notes:** _______________

## 4. Code Quality & Readability

**Definition:** Is the code clean, readable, consistent with the codebase, and reasonably efficient?

**What to check:**
- Readability: clear names, function boundaries, and structure
- Consistency: follows repo conventions and idioms
- Efficiency: avoids needless performance issues (e.g., O(n) hot paths)
- Maintainability: organized, avoids unnecessary complexity

1 — Messy, confusing, or unmaintainable.
2 — Hard to read, inconsistent with repo style, or inefficient.
3 — Understandable but inconsistent, cluttered, or slightly inefficient.
4 — Mostly clear, with minor style or efficiency issues.
5 — Clean, idiomatic, consistent, and efficient enough for the context.


**Score:** ___
**Notes:** _______________

## 5. Testing (Coverage & Quality)

**Definition:** Are tests added or updated appropriately, and do they verify the new code effectively?

**What to check:**
- Meaningful tests for new features or fixes
- Edge cases included
- Tests are well-placed and consistent with existing structure
- Existing tests still pass

1 — No tests or failing tests.
2 — Weak or incorrectly structured tests.
3 — Basic or incomplete tests with coverage gaps.
4 — Good tests, missing only minor edge cases.
5 — Comprehensive, well-written tests with excellent coverage.


**Score:** ___
**Notes:** _______________
