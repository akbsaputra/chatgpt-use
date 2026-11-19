# Findings and the numbers behind each section

All figures come from OpenAI Signals v3.0 (July 2024 to September 2026) via `scripts/build_data.py`. Quarterly figures are averages of monthly shares. "SEA" is the simple average of Indonesia's neighbors with complete data, excluding Indonesia.

## Work share (sections `opening`, `hundred`, `drift`)

| | Q3 2024 | Q3 2026 |
| --- | --- | --- |
| Indonesia | 45.2% | 39.9% |
| SEA average (9 countries) | 44.1% | 32.6% |
| World | 48.9% | 30.7% |

1. Indonesia fell to 35.9% in Q1 2025, then moved between 36% and 43%.
2. Rank on work share: about 78th of roughly 150 in the second half of 2024, 4th of 145 over April to September 2026 (behind Singapore, Peru, and Zimbabwe).
3. Change from the first six months to the last six: Indonesia -1.5 points, SEA -9.8, world -15.2, median country -14.8. Indonesia is 2nd of 138 countries with complete data.
4. The nine neighbors, Q3 2024 then Q3 2026: Singapore 67.7% to 42.9%, Malaysia 50.9% to 34.4%, Myanmar 34.4% to 18.0%, Brunei 51.7% to 35.9%, Cambodia 39.6% to 32.2%, Thailand 41.2% to 34.0%, Laos 28.8% to 22.1%, Vietnam 39.6% to 34.7%, Philippines 42.7% to 38.8%. All nine fell. Used in the Southeast Asia block of `drift`.

5. World only, three-way label (work, schoolwork, other), Q3 2024 then Q3 2026: work 25.3% to 20.1%, schoolwork 25.8% to 11.9%, other 48.9% to 68.0%. Not published by country. Used in `hundred` to show that the binary "work" label takes in schoolwork.

## Per-capita rank (section `crowd`)

1. Indonesia is 117th of 173 in Q3 2026, and between 112th and 119th since Q1 2025. So 116 countries rank above it and 56 below. Only ranks are published, not counts.
2. Azerbaijan 1st, Singapore 2nd, United States 49th, Malaysia 66th, Brunei 68th, Philippines 93rd, Vietnam 99th, Thailand 106th, India 119th, Cambodia 132nd, Timor-Leste 139th, Myanmar 142nd, Laos 146th, South Sudan 173rd.

## Topics (sections `hundred`, `desk`, `closing`)

Share of all messages, Q3 2024 then Q3 2026.

| Topic | Indonesia | SEA | World |
| --- | --- | --- | --- |
| Writing | 30.9 → 28.5 | 37.7 → 29.3 | 33.6 → 21.2 |
| Practical guidance | 32.2 → 28.4 | 25.1 → 27.5 | 26.7 → 29.4 |
| Seeking information | 17.8 → 13.8 | 15.2 → 14.9 | 16.6 → 20.1 |
| Multimedia | 2.1 → 10.4 | 2.2 → 7.9 | 2.6 → 8.3 |
| Self-expression | 4.2 → 8.6 | 6.1 → 9.8 | 4.3 → 9.2 |
| Technical help | 9.9 → 4.6 | 10.0 → 3.7 | 12.5 → 4.3 |
| Other or unknown | 2.9 → 5.9 | 3.7 → 6.9 | 3.6 → 7.5 |

1. Writing rank, April to September 2026: 16th of 146. Seeking information: 139th of 146.
2. The "hundred messages" grid uses largest-remainder rounding: 28, 28, 14, 10, 9, 5, 6 for 2026 and 31, 32, 18, 2, 4, 10, 3 for 2024.
3. Important nuance: the region now writes as much as Indonesia. The difference is that the region fell 8 points and Indonesia fell 2.

## Intent (section `tell`)

Work-related messages, April to September 2026.

| | Asking | Doing | Expressing |
| --- | --- | --- | --- |
| Indonesia | 30.7% | 53.6% | 15.7% |
| SEA average (7 countries) | 31.0% | 48.1% | 20.9% |
| World | 31.2% | 46.5% | 22.2% |

1. Indonesia is 7th of 119 on doing and 118th of 119 on expressing. Japan is 1st on expressing (29.4%).
2. Doing share of work messages, Q3 2024 to Q3 2026: world 52.7% to 46.4%, Indonesia 52.6% to 53.5%.

## Work activities (section `campus`)

Share of work-related messages, average of Q4 2025 to Q3 2026, 84 countries.

| Activity (O*NET) | Indonesia | SEA (5) | Median | Rank |
| --- | --- | --- | --- | --- |
| Develop research plans or methodologies | 2.56 | 1.03 | 0.52 | 1 |
| Present research or technical information | 1.28 | 0.62 | 0.48 | 1 |
| Evaluate scholarly work | 1.33 | 0.69 | 0.55 | 2 |
| Analyze scientific or applied data | 0.99 | 0.63 | 0.65 | 2 |
| Prepare informational or instructional materials | 8.21 | 4.59 | 3.99 | 3 |
| Edit written materials or documents | 18.08 | 19.80 | 15.65 | 25 |
| Obtain information about goods or services | 1.46 | 1.93 | 2.51 | 83 |
| Advise others on legal or regulatory matters | 0.48 | 1.02 | 1.55 | 81 |

1. Seven research-and-teaching activities (the first five above plus "develop educational programs" and "teach academic or vocational subjects") sum to 18.0% for Indonesia, 10.9% for SEA, and 9.3% for the median country. Indonesia is 2nd of 84.
2. The country-level classifier cannot separate study from work, so this is a reading, not a proof.

## Age (section `young`)

1. Share of messages from adults 18 to 24: Indonesia 62.9% to 43.8%, SEA (8 countries) 48.0% to 37.0%, world 41.0% to 30.3%.
2. September jumps in Indonesia's monthly under-25 share: +5.5 points in 2024, +2.2 in 2025, +6.8 in 2026.
3. Age mix in Q3 2026 (18-24, 25-34, 35-44, 45-54, 55-64, 65+): Indonesia 43.8, 36.8, 11.9, 4.6, 1.5, 1.5. SEA 37.0, 37.2, 15.7, 5.8, 2.2, 2.1. World 30.3, 35.0, 18.9, 9.3, 3.9, 2.6.
4. Same mix for the eight large countries in the age table: India 44.4, 32.9, 14.1, 4.7, 1.6, 2.3. Nigeria 42.8, 36.8, 11.9, 4.7, 1.9, 2.0. Mexico 33.0, 38.9, 16.8, 7.2, 2.5, 1.6. Brazil 26.1, 36.7, 21.7, 10.0, 3.4, 2.0. Japan 25.0, 32.9, 20.0, 14.3, 5.9, 1.9. Germany 23.6, 35.9, 22.2, 10.6, 5.1, 2.7. United States 21.4, 32.7, 22.7, 12.9, 6.8, 3.5. South Korea 17.2, 33.1, 24.4, 14.9, 7.2, 3.1. The phone layout joins the last three groups into "45 and over": Indonesia 7.6, Southeast Asia 10.1, world 15.8, India 8.6, Nigeria 8.6, Mexico 11.4, Brazil 15.5, Japan 22.1, Germany 18.3, United States 23.2, South Korea 25.2.
5. Indonesia's 18 to 24 share ranks 22nd of 141 countries with all six age groups in each month of Q3 2026.
6. Indonesia's 25-to-34 share grew from 23.6% to 36.8%.

## Gender by first name (section `women`)

1. Feminine-name share: Indonesia 53.4% in July 2024 and 60.7% in Q3 2026. SEA (6 countries) 45.9% to 50.1%. World 42.2% in July 2024, crossing 50% in May 2025, 52.1% in Q3 2026.
2. Indonesia is 6th of 107 countries with complete data over April to September 2026.
3. By topic in Q3 2026, Indonesia then world: self-expression 66.7 and 60.6, writing 65.6 and 56.4, practical guidance 61.5 and 53.5, multimedia 57.1 and 50.7, other 54.9 and 47.8, seeking information 53.4 and 47.0, technical help 50.3 and 37.7.

## Pictures (section `pictures`)

1. "Create visual designs or displays" as a share of Indonesia's work messages: 2.7% in Q1 2025, 10.6% in Q3 2026. SEA 8.8%, median country 7.5%.
2. Programming: 6.1% to 3.0%. Design passed programming between Q4 2025 and Q1 2026. The same crossing falls in the same interval for the Southeast Asia average (design 3.2% then 4.3%, programming 4.7% then 3.4%) and for the median country (design 4.1% then 4.8%, programming 4.5% then 3.2%). In Q3 2026 programming stands at 2.6% for the region and 3.0% for the median country.
3. Multimedia as a share of all Indonesian messages jumped from 3.9% in March 2025 to 10.5% in April 2025.

## Closing (section `closing`)

No new figures. The closing paragraphs reuse numbers from the sections above: the world's work share (48.9% to 30.7%), Indonesia's change rank (2nd smallest loss of 138), writing (28.5% against 21.2%), doing ahead of asking (53.6% doing, 15.7% expressing, so 30.7% asking), under-25 share (43.8%), feminine-name share (60.7%), per-capita rank (117th of 173), month-to-month noise in the work share (about 4 points), and visual design (2.7% to 10.6%).

## Outside sources used

The full list with links is at the end of `src/template.html`.

1. Population and rank: Databoks (World Population Review), October 2026.
2. Top-five market and tripled weekly users: Marketing-Interactive, September 2025.
3. Global shift to non-work use: Chatterji et al., NBER Working Paper 34255.
4. Student numbers, largest field of study, and share of women: GoodStats, from ministry statistics for 2025.
5. Student AI use: Tirto and Jakpat survey, May 2024.
6. Thesis rule: Hukumonline and Antara on Permendikbudristek No. 53 of 2023.
7. Teachers drafting modules with AI: Universitas Airlangga.
8. Academic calendar: Universitas Gadjah Mada, 2026/2027.
9. Image generator launch date: Gigazine, April 2025.
