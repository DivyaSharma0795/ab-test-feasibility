# The Math Behind the Calculator (No Stats Degree Required)

This guide explains every number the calculator uses through one running story about soda. Read it top to bottom once, then use it as a reference.

**The big idea in one sentence:** before you run a test, the MDD tells you the *smallest real difference your test would reliably notice*. If the difference you care about is smaller than that, the test is **not feasible** as designed (see [section 7](#7-is-my-test-feasible)).

---

## 1. The story: Coke vs. Pepsi

You run a taste-test booth. Each visitor is randomly handed a blind sample of **Coke** or **Pepsi** and asked: *"Would you buy this?"*

- From past booths, about **40% say yes to Coke**. This is the **baseline**.
- You want to know whether Pepsi does better or worse.
- You can test **2,000 people** (1,000 per drink).

The question this whole document answers: **how different does Pepsi have to be from Coke for this booth to spot it?** That threshold is the **Minimum Detectable Difference (MDD)**.

---

## 2. Why can't we just compare the two percentages?

Because of **luck**. Suppose Coke and Pepsi are *exactly* equally liked. If you sample 1,000 people per drink, you won't get exactly 40% and 40%. You might see 41.2% vs. 38.9%, purely by chance. Every sample is a slightly random snapshot.

So when you see a gap, there are two explanations:

1. **Real difference:** one drink really is more popular.
2. **Noise:** you happened to sample slightly different crowds.

All of A/B testing math is a way to decide, fairly, how big a gap must be before we stop blaming noise.

---

## 3. Standard error: how much the result wobbles

The **standard error (SE)** measures how much a result typically wobbles from luck alone.

For a yes/no question, one person's "spread" is `p × (1 - p)`. At p = 40% that's `0.4 × 0.6 = 0.24`. This is the **variance**. It is biggest at 50% (0.25) and shrinks as p nears 0% or 100%.

The wobble of the *difference between two groups* is:

```
SE = sqrt( variance × (1/n_coke + 1/n_pepsi) )
   = sqrt( 0.24 × (1/1000 + 1/1000) )
   = sqrt( 0.00048 )
   ≈ 0.0219      (about 2.2 percentage points)
```

So even if the drinks are identical, the gap between the two groups will typically land within about ±2.2 points. Notice that **more people means a smaller SE**, because the `1/n` terms shrink.

---

## 4. Alpha (α): the false-alarm dial

Suppose there is no real difference. We still don't want to shout "Pepsi wins!" every time luck produces a gap. **Alpha is how often we accept being fooled like that.** The usual choice is **α = 0.05**, meaning a 5% false-alarm rate.

Think of a smoke alarm. Alpha is how often it goes off when there's no fire. Lower alpha means fewer false alarms, but a less sensitive alarm.

To achieve α = 5% (two-tailed), the gap must be at least **1.96 standard errors** away from zero. That 1.96 is called a **z-score**, a distance measured in SE units. It comes from the bell curve: only 5% of pure-luck results land more than 1.96 SEs from zero, in either direction.

```
z_alpha = 1.96   (for alpha = 0.05, two-tailed)
```

---

## 5. Power (1 - β): the catch-a-real-fire dial

Now suppose there *is* a real difference. Will our test catch it? **Power is the probability that it does.** The usual target is **80%**. The remaining 20% is **β (beta)**, the chance we miss a real effect. A missed effect is a "false negative."

In the smoke-alarm picture, power is how often the alarm rings when there really is a fire.

To catch a real effect 80% of the time, the *true* gap must sit an extra **0.84 standard errors** beyond the alarm threshold:

```
z_power = 0.84   (for power = 0.80)
```

Why 0.84? If the true gap is exactly at the threshold, luck pushes your result below it half the time (50% power). Sliding the true gap 0.84 SEs above the threshold means only 20% of the wobble drags you back under it, which gives 80% power.

---

## 6. Putting it together: the MDD

The true gap must cover both jobs, clearing the false-alarm bar (`z_alpha`) and the catch-it-reliably margin (`z_power`):

```
MDD = (z_alpha + z_power) × SE
    = (1.96 + 0.84) × 0.0219
    ≈ 0.0614
```

**Result:** with 1,000 people per drink and Coke at 40%, the test can reliably detect a Pepsi that differs by about **6.1 percentage points** (Pepsi at roughly 46% or 34%). Relative to the 40% baseline, that's a **15.3% relative lift**.

What this does and doesn't say:

- If Pepsi is truly 6 points better, you'll catch it about 80% of the time.
- If Pepsi is only 2 points better, this test will *probably miss it*. That isn't a flaw in the drinks, just a test too small for that question.
- So if you care about 2-point differences, this design is **not feasible**, and that is exactly what the calculator's verdict tells you.

---

## 7. Is my test feasible?

This is the question the calculator's verdict answers, so here is the exact rule.

> **A test design is *feasible* when its MDD is no bigger than the smallest lift you would act on.**
> **It is *not feasible* when its MDD is bigger than that.**

```
MDD ≤ minimum useful lift   →  Feasible
MDD >  minimum useful lift  →  Not feasible
```

### Where does the "minimum useful lift" come from?

It comes from the business, not from statistics. It is the smallest improvement that would change what you do: the point where rolling out the change pays for itself, or where the team would bother acting. Examples: "Below +5 points we wouldn't switch drinks," or "under a 10% relative increase in sign-ups isn't worth the engineering work."

Decide it **before** you look at the MDD. If you pick it afterwards, it's tempting to choose whatever number makes the test look feasible.

### The bathroom-scale picture

The MDD is how finely your scale can read. The minimum useful lift is the change you need to see.

- Scale reads to the nearest **6 lb** and you need to see a **7 lb** change → the scale is good enough. **Feasible.**
- Scale reads to the nearest **8 lb** and you need to see a **7 lb** change → the scale can't do it. **Not feasible.**

### Worked example (soda booth)

Suppose you would only switch drinks if Pepsi beats Coke by **at least 7 percentage points** (7 points on a 40% baseline is a 17.5% relative lift). You have 2,000 people.

| Design | People per group | MDD | vs. 7-point threshold | Verdict |
|---|---|---|---|---|
| Coke vs. Pepsi | 1,000 | 6.1 pts | 6.1 ≤ 7 | **Feasible** |
| + Sprite (3 groups) | 667 | 8.3 pts | 8.3 > 7 | **Not feasible** |
| + Sprite + Fanta (4 groups) | 500 | 10.0 pts | 10.0 > 7 | **Not feasible** |

Adding one more drink flipped the verdict, even though the audience stayed the same. Nothing about the drinks changed. The extra groups made the test blurrier (fewer people per group, stricter alpha).

### The same rule from the other side: audience needed vs. audience available

Feasibility can also be checked with the reverse-mode formula from [section 13](#13-reverse-mode-how-many-people-do-i-need). Both are the same equation rearranged, so they always agree.

```
Feasible  ⇔  audience available ≥ audience required
```

| Threshold (smallest lift you'd act on) | Groups | People required | People available | Available / required | Verdict |
|---|---|---|---|---|---|
| 7 pts | 2 | 1,538 | 2,000 | 130% | Feasible |
| 7 pts | 3 | 2,793 | 2,000 | 72% | Not feasible |
| 5 pts | 2 | 3,014 | 2,000 | 66% | Not feasible |
| 3 pts | 2 | 8,372 | 2,000 | 24% | Not feasible |

The "available / required" percentage tells you *how far off* a not-feasible test is. At 72% you're fairly close. At 24% you would need more than four times the audience.

### What the verdict does and doesn't mean

- **Not feasible does not mean "there is no difference."** It means *this design can't reliably tell*. The drinks might differ a lot. You just can't find out with this setup.
- **Feasible does not mean "you will find something."** If the true lift is exactly your threshold, you catch it about 80% of the time (that's what 80% power means). If the true lift is smaller, you'll probably miss it. If it's larger, you're more likely to catch it.
- **Close calls deserve caution.** If the MDD is only a hair below your threshold, treat the test as borderline. A small change to your assumptions could flip it.
- **The verdict depends on your inputs.** A wrong baseline rate or an over-optimistic response rate will make a test look more feasible than it is.

### If the answer is "not feasible": what can you change?

| Lever | Effect | Trade-off |
|---|---|---|
| More people, or run longer | Biggest lever (4× people → half the MDD) | Time, cost, audience limits |
| Fewer groups | More people per group, fewer comparisons | Test fewer ideas at once |
| Even 50/50 split | Most efficient use of a fixed audience | Less protection if the treatment is risky |
| Higher share measured (response rate) | More people in the analysis | May be hard to influence |
| One-tailed test | About 11% smaller MDD in our example | Can't detect harm; see [section 9](#9-one-tailed-vs-two-tailed) |
| Less noisy metric or variance reduction (for example, using each person's pre-test behaviour) | Smaller variance, smaller MDD | Extra analysis work |
| Raise the minimum useful lift | Makes the same MDD acceptable | Only fair if you truly wouldn't act on smaller gains |
| Lower power or higher alpha | Smaller MDD | More missed effects or false alarms. Use as a last resort |

### Where you'll see this in the tool

- **Streamlit and web page:** the **Verdict** card compares the relative MDD with your *Minimum useful relative lift*. The group-comparison table shows Yes/No for 2 to 6 groups. In reverse mode, "audience available vs. required" above 100% means you have enough.
- **Excel:** the *Verdict* cell (forward mode), the *Feasible?* column in the group table, and *Enough audience?* (reverse mode). If you leave *Minimum useful relative lift* blank, the verdict shows "n/a".

---

## 8. What makes the MDD bigger or smaller?

Still Coke at 40%, two groups, α = 0.05 two-tailed, 80% power unless stated:

| Change | MDD | Takeaway |
|---|---|---|
| 500 people total | 12.3 pts | Small tests only catch big effects |
| **2,000 people total (our booth)** | **6.1 pts** | |
| 8,000 people total | 3.1 pts | **4× the people → half the MDD** |
| Power 90% instead of 80% | 7.1 pts | Being more certain costs sensitivity |
| Alpha 0.01 instead of 0.05 | 7.5 pts | Fewer false alarms costs sensitivity |

The key relationship is that **the MDD shrinks with the *square root* of the sample size**. To detect an effect half as big, you need *four times* the people. This is the most useful rule of thumb in test planning.

---

## 9. One-tailed vs. two-tailed

- **Two-tailed:** "Is Pepsi *different* from Coke, better or worse?" The false-alarm budget is split across both directions.
- **One-tailed:** "Is Pepsi *better* than Coke?" You only look in one direction, so the whole budget goes to that side.

For α = 0.05, `z_alpha` drops from 1.96 (two-tailed) to 1.645 (one-tailed). With our booth:

```
One-tailed: (1.645 + 0.84) × 0.0219 ≈ 0.0545   →  5.5 points (vs. 6.1 two-tailed)
```

That's more sensitive, but it comes with a cost. A one-tailed test **cannot flag Pepsi being worse**. Use it only if a result in the other direction would lead to the same action as no result. If you would want to know when the new thing hurts, use two-tailed.

---

## 10. Adding Sprite: more than two groups

Now the booth also hands out **Sprite**. Coke remains the control, and you compare Pepsi vs. Coke *and* Sprite vs. Coke. That's **k = 3 groups** and **m = k - 1 = 2 comparisons**.

### Problem 1: the false-alarm budget gets used twice

Each comparison has a 5% chance of a false alarm. With two comparisons, the chance that *at least one* is a false alarm rises to:

```
1 - 0.95 × 0.95 = 9.75%      (with 5 comparisons: 22.6%)
```

It's like buying two lottery tickets. Your chance of winning something is higher than with one ticket. Here, "winning" means being fooled by luck.

### The fix: adjust alpha for each comparison

- **Bonferroni:** split the budget evenly. `alpha per comparison = 0.05 / 2 = 0.025`.
- **Šidák:** a slightly more exact version: `1 - (1 - 0.05)^(1/2) = 0.02532`. It is nearly the same as Bonferroni.

A stricter alpha means a bigger `z_alpha`: **2.241** instead of 1.96.

### Problem 2: fewer people per group

Same 2,000 people, but now split three ways: about **667 per drink**.

```
SE        = sqrt( 0.24 × (1/667 + 1/667) ) ≈ 0.0268
MDD       = (2.241 + 0.842) × 0.0268 ≈ 0.0827     →  8.3 points (20.7% relative)
```

| Groups | People per group | MDD (Coke baseline 40%) |
|---|---|---|
| 2 (Coke, Pepsi) | 1,000 | 6.1 pts |
| 3 (+ Sprite) | 667 | 8.3 pts |
| 4 (+ Fanta) | 500 | 10.0 pts |

**Adding groups hurts twice:** each group gets fewer people *and* each comparison gets a stricter alpha. This is why the calculator's comparison table exists. It shows the point where adding another arm makes the test infeasible.

---

## 11. Unequal splits and response rates

### Unequal split

Sometimes you can't give half the people the new thing, for example a risky offer that only goes to 20%. With **20% Coke / 80% Pepsi** (400 vs. 1,600):

```
SE  = sqrt( 0.24 × (1/400 + 1/1600) ) ≈ 0.0274
MDD = 2.80 × 0.0274 ≈ 0.0767      →  7.7 points (vs. 6.1 at 50/50)
```

The smaller group is the bottleneck. An even split is the most efficient for a fixed audience.

### Response rate ("share measured")

Suppose you email 6,667 customers, but only **30% respond**. Only responders can be analysed, so:

```
analysed sample = 6,667 × 0.30 = 2,000  →  same MDD as the booth (6.1 pts)
```

The calculator's **Share measured** input does exactly this multiplication. One caution: responders may differ from non-responders (for example, people who answer a soda survey may love soda). The math can't fix that.

---

## 12. Numbers that aren't percentages

What if the metric is *cans of soda per week* rather than yes/no? The formula is unchanged. Only the variance changes. Instead of `p(1 - p)`, use the square of the **standard deviation (σ)**, which is how spread out people's values are.

Say Coke drinkers average **5 cans/week** with σ = 3 cans, and you have 2,000 people (two equal groups):

```
SE  = sqrt( 3² × (1/1000 + 1/1000) ) = sqrt(0.018) ≈ 0.134
MDD = 2.80 × 0.134 ≈ 0.376 cans      →  7.5% of the 5-can baseline
```

Noisier metrics (bigger σ) need bigger samples. If everyone drinks almost exactly 5 cans, tiny differences are easy to spot. If people range from 0 to 20, they aren't.

---

## 13. Reverse mode: "How many people do I need?"

Now flip it around. Suppose a difference smaller than **3 percentage points** isn't worth acting on. How many people do you need? Solve the MDD equation for the sample size:

```
N = (z_alpha + z_power)² × variance × ( 1/c + (k - 1)/(1 - c) ) / Δ²
```

Here Δ is the difference to detect and c is the control share. For two equal groups (c = 0.5, k = 2), the bracket equals 4:

```
N = 2.80² × 0.24 × 4 / 0.03²
  = 7.85 × 0.24 × 4 / 0.0009
  ≈ 8,372 people     →  about 4,186 per drink
```

With Sprite added (3 groups, Bonferroni), the same 3-point goal needs about **15,208 people (roughly 5,069 per drink)**, nearly double.

Remember the square-root rule: cutting the target difference in half quadruples the sample. Reverse mode helps you spot quickly that "detect a 1-point change" may need an audience you don't have.

---

## 14. Why there is no degrees-of-freedom input

Classic textbooks use the **t-distribution**, whose shape depends on "degrees of freedom" (roughly, sample size minus the number of groups). It has slightly fatter tails than the bell curve because small samples are less certain.

Once you have more than about 100 people per group, the t-distribution and the normal (z) distribution are almost indistinguishable. For example, the two-tailed 5% cutoff is 1.984 with 100 degrees of freedom vs. 1.960 for z. Marketing tests typically have thousands, so the calculator uses the simpler z-score. If you plan a tiny test (tens of people), use an exact power tool such as `statsmodels`.

---

## 15. Assumptions and limitations

1. **Normal approximation.** Works well for reasonably large samples and rates that aren't extremely close to 0% or 100%.
2. **Variance at the baseline.** The calculator uses the control group's `p(1 - p)` for both groups. If the treatment changes the rate a lot, the true variance shifts slightly.
3. **Independent people.** If your data is clustered (for example, several people from one household or store), the effective sample is smaller than it looks.
4. **One look at the end.** Peeking at results repeatedly and stopping when you see significance inflates false alarms. Plan the sample, then wait.
5. **Each treatment vs. control.** The tool doesn't do an "any difference among all groups" test (ANOVA/Cohen's f).
6. **MDD is not a prediction.** A 6-point MDD doesn't mean you'll *see* 6 points. It means a *true* 6-point difference would be caught 80% of the time.
7. **Statistical vs. practical significance.** Detecting a difference doesn't mean it's worth acting on. Decide your minimum useful lift *first*.

---

## 16. Cheat sheet

| Term | Plain meaning | Typical value |
|---|---|---|
| Baseline (p) | How the control group normally behaves | Your data |
| Variance | How spread out individuals are: `p(1 - p)` or `σ²` | 0.24 at 40% |
| Standard error | How much a result wobbles from luck | 0.0219 in our booth |
| Alpha (α) | Accepted false-alarm rate | 0.05 |
| Power (1 - β) | Chance of catching a real effect | 0.80 |
| z-score | A distance measured in SE units | 1.96, 0.84 |
| MDD | Smallest true difference the test reliably catches | 6.1 pts in our booth |
| Minimum useful lift | Smallest improvement you'd act on (a business decision) | Your call |
| Feasible | MDD ≤ minimum useful lift (equivalently, audience available ≥ required) | Yes / No |
| k / m | Groups / comparisons against control (m = k - 1) | 2 / 1 |
| Bonferroni / Šidák | Ways to tighten alpha when m > 1 | α / m |

**The one formula:**

```
MDD = (z_alpha + z_power) × sqrt( variance × (1/n_control + 1/n_treatment) )
```

**Three rules of thumb:**
1. 4× the people → half the MDD.
2. Every extra group costs you sensitivity twice (fewer people each, stricter alpha).
3. Decide the smallest lift worth acting on *before* the test. If the MDD is bigger than that, the test is not feasible as designed.
