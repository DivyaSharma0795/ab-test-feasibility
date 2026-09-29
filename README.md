# Test Feasibility Calculator

**Find out whether your A/B test can detect a real difference, *before* you run it.**

*(Technically: an MDD and sample-size calculator for A/B tests, with Streamlit, web and Excel versions.)*

---

## Start here: what problem does this solve?

Imagine a bathroom scale that only shows weight to the nearest 10 pounds. You go on a diet and lose 2 pounds, but the scale still shows the same number. The scale isn't broken. It just can't see a change that small.

**A/B tests have the same problem.** Every test has a *smallest difference it can reliably see*. If the improvement you're hoping for is smaller than that, the test will probably say "no difference," even when your idea works. You can spend weeks and end up throwing away a good idea.

This calculator tells you, **before you start**, how small a difference your test can see and whether that's good enough. That answer is called the **MDD** (minimum detectable difference). It also gives a plain verdict: **feasible** or **not feasible**.

## How you'd use it: a 3-minute example

**Scenario:** A streaming service wants to test a win-back email to lapsed subscribers. About **4%** of lapsed subscribers normally come back. There are **50,000** people available for the test.

**Step 1: Decide the smallest improvement worth acting on.**
This is a business call. The team says: *"We'd only roll this out if it lifts the come-back rate by at least 15% relative, from 4.0% to 4.6%."*

**Step 2: Enter what you know.**

| Input | Value |
|---|---|
| Metric type | Proportion (yes/no: did they come back?) |
| Audience size | 50,000 |
| Baseline rate | 4% |
| Groups | 2 (old email vs. new email) |
| Alpha / power | 0.05 / 0.80 (the standard defaults) |
| Minimum useful lift | 15% |

**Step 3: Read the result.**

> With 25,000 people per group, this test can reliably detect a lift of **0.49 percentage points (12.3% relative)**.
> That is smaller than your 15% threshold, so the test is **feasible** ✅

**Step 4: Now try a "what if?"** The team asks: *"Can we test two new subject lines against the old one?"* Change groups from 2 to 3:

> With 3 groups, the smallest detectable lift grows to **16.5% relative**.
> That is bigger than your 15% threshold, so the test is **not feasible** ❌
> Reverse mode says you'd need about **60,800 people**, and you have 50,000 (82% of what's needed).

Now you can choose *before launch*: drop back to two emails, get a bigger audience, or accept that you can only detect bigger lifts. That is the whole point of the tool.

## What does "feasible" mean?

> **Feasible** = the smallest difference your test can detect is **no bigger than** the smallest improvement you'd act on.
> **Not feasible** = your test is too blurry to see the improvement you care about.

Not feasible doesn't mean your idea doesn't work. It means *this test design can't tell*. The full explanation, with a worked example and a list of ways to fix a "not feasible" test, is in [MATH.md, section 7](docs/MATH.md#7-is-my-test-feasible).

## Words you'll see

| Term | In plain English |
|---|---|
| **Baseline** | How the normal (control) group behaves today, for example a 4% come-back rate |
| **Lift** | How much better (or worse) the new version does, in points or as a percentage of the baseline |
| **MDD** | The smallest lift your test can reliably detect |
| **Minimum useful lift** | The smallest lift you'd actually act on (your call, not the calculator's) |
| **Alpha** | How often you accept being fooled by luck (usually 5%) |
| **Power** | How often you catch a real effect (usually 80%) |

Want the story behind these, told with Coke, Pepsi and Sprite? Read **[docs/MATH.md](docs/MATH.md)**. It needs no prior stats knowledge.

---

## Which version should I use?

The three versions do the same thing and use the same math.

| Version | Use this if... | File |
|---|---|---|
| **Excel workbook** | You or your stakeholders prefer spreadsheets | `excel/mdd_calculator.xlsx` |
| **Web page** | You want to send someone a link, with nothing to install | `web/index.html` |
| **Streamlit app** | You want the full tool and the ability to extend it in Python | `app.py` |

## What you get

- **Forward mode:** "Given my audience and design, what can I detect?" It returns the MDD (in points and as a percentage), people per group, and the feasible / not-feasible verdict.
- **Reverse mode:** "I want to detect a 3% lift. How many people do I need?" It returns the required audience and compares it with what you have.
- **Group comparison table:** the MDD for 2 to 6 groups side by side, so you can see when adding another arm stops being worth it.
- **Chart:** the MDD against audience size, so you can see how much audience you need to reach your target.
- **Design options:** yes/no or numeric metrics, one- or two-tailed tests, uneven splits (such as 10% control), a "share measured" input for response rates, and a multiple-comparison correction (Bonferroni, Šidák or none).

## Quick start

### Excel
Open `excel/mdd_calculator.xlsx` and edit the yellow cells (blue text). Everything else updates. The starting values (200,000 audience, 5% baseline) are only examples.

### Web page
Open `web/index.html` in any browser. It is one file with no dependencies.

To publish it as a link, push the repo to GitHub, then choose **Settings → Pages → Source: GitHub Actions**. The included workflow deploys the `web/` folder on every push to `main`.

### Streamlit app
```bash
git clone https://github.com/divyasharma0795/ab-test-feasibility.git
cd ab-test-feasibility
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
To host it for free, deploy the repo on [Streamlit Community Cloud](https://streamlit.io/cloud) with `app.py` as the entry point.

## Inputs

| Input | Meaning | Typical value |
|---|---|---|
| Metric type | *Proportion* (yes/no: converted, responded) or *Continuous* (spend, balance; needs a standard deviation) | |
| Audience size | Everyone you could put in the test | |
| Share measured | The fraction who end up in the analysis, such as the response rate | 100% if everyone counts |
| Baseline rate / mean | What "normal" looks like in the control group | From your data |
| Groups | Control plus treatments; 2 is a classic A/B test | 2 |
| Control share | Blank for an equal split, or something like 10% control / 90% treatment | Equal |
| Alpha | The false-alarm rate you accept | 0.05 |
| Power | The chance of catching a real effect | 0.80 |
| Test type | Two-tailed ("different") or one-tailed ("better" only) | Two-tailed |
| Correction | How to tighten alpha when comparing several groups to control | Bonferroni |
| Minimum useful lift | The smallest lift you'd act on; this drives the verdict | Your call |

There is no degrees-of-freedom input. At A/B-test sample sizes it makes no practical difference; [MATH.md explains why](docs/MATH.md#14-why-there-is-no-degrees-of-freedom-input).

## Under the hood

Each treatment group is compared with control (m = k − 1 comparisons):

```
MDD = (z_alpha + z_power) × sqrt( variance × (1/n_control + 1/n_treatment) )

variance = p(1 − p)   for a yes/no metric
variance = sigma²     for a numeric metric

Feasible  ⇔  MDD ≤ minimum useful lift
```

Reverse mode solves the same equation for the sample size:

```
N = (z_alpha + z_power)² × variance × ( 1/c + (k−1)/(1−c) ) / Δ²      (c = control share, Δ = lift to detect)
```

## Project structure

```
├── app.py                  Streamlit app
├── mdd_calc/core.py        The math (shared by the app and the tests)
├── web/index.html          Standalone web calculator
├── excel/                  Excel calculator (live formulas)
├── docs/MATH.md            Beginner-friendly explanation of the statistics
├── tests/test_core.py      Unit tests against hand-checked values
└── .github/workflows/      Automatic tests + GitHub Pages deploy
```

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

The tests check the core functions against hand-checked values (for example, a 200,000 audience at a 5% baseline gives a 5.46% relative MDD) and confirm that forward and reverse modes are exact inverses.

## Assumptions and limitations

- Uses the normal approximation with variance taken at the baseline. That's standard for feasibility checks but is not an exact power calculation for very small samples or rates near 0% or 100%.
- Assumes independent observations (no clustering) and one look at the results at the end (no peeking).
- Compares each treatment with control. It doesn't run an overall test across all groups.
- The MDD is a planning tool, not a forecast. It says what your test *could* detect, not what you *will* see.

Details are in [MATH.md, section 15](docs/MATH.md#15-assumptions-and-limitations).

## License

MIT. See [LICENSE](LICENSE).
