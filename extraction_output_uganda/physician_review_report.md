# Clinical Verification Report — WHO Consolidated Malaria Guidelines
## Stage 4b: Physician Review Package

**Generated:** 2026-03-12T13:34:48Z | **Pipeline version:** 4b
**Source:** Uganda-Clinical-Guidelines-20231.pdf (1161 pages)
**Safety rule:** No content proceeds to deployment without `verified_by` signature + `audit_hash`.

---

## How to Use This Document

1. Review each item against the **5 Clinical Verification Checks**:
   - **Dosage Accuracy**: Dose values match source PDF exactly (e.g., '80+480 mg', '1 tablet').
   - **Stratification**: Age/weight ranges are preserved — no merged or missing rows.
   - **Contraindications**: Warnings are present (e.g., 'Do not use in first trimester').
   - **Conditional Logic**: IF/THEN referral logic is intact (e.g., NLL dosing rules, danger sign criteria).
   - **Provenance**: Source page number and section citation are correctly cited.
2. For each check, mark: ✅ Pass | ❌ Fail | ⚠️ Corrected | — Not applicable
3. Record your **overall decision**: Approved / Flagged / Corrected
4. Enter corrections in the notes field if flagging or correcting
5. Fill in your reviewer details (name, role, institution, date)

---

## Review Summary

| Tier | Description | Chunks | Priority | Est. Time |
|---|---|---|---|---|
| 1. Validated dosing tables | Passed all 6 Stage 3 automated plausibility checks. Physicia... | 0 | Mandatory | ~0 min |
| 2. Unvalidated dosing tables | NOT validated by Stage 3 automated checks (no weight column ... | 3 | Mandatory | ~6 min |
| 3. Clinical management tables | Safety-critical clinical management content. Full manual rev... | 0 | Mandatory | ~0 min |
| 4. Evidence tables + high-priority narratives | Contains clinical thresholds, dosing keywords, or contraindi... | 242 | Recommended | ~2.0 hrs |
| **Total mandatory** | | **3** | | **~6 min** |

**Total review items:** 245 (mandatory: 3, recommended: 242). Optional chunks not included: 3490.

---

## TIER 2 — Unvalidated Dosing Tables (3 chunks) — MANDATORY REVIEW

> ⚠️ These tables were NOT validated by Stage 3 automated checks (no weight column identified or checks not applicable). Extra care required — verify all values against the source PDF.

### 1. stitched_table-S1
**Pages:** 229, 230 | **Section:** 5.2.1.1.2 Dosing of ACTs
**Validation:** No validation data | **Condition:** Malaria | **Dosage:** 17 days, oral

**Audit hash:** `362a1e3e16468900...`

#### Extracted Content
```
| TREATMENT | LOC |
| --- | --- |
| Cutaneous Leishmaniasis (all patients)  Frequently heals spontaneously but if severe or persistent, treat as for Visceral Leishmaniasis below Visceral Leishmaniasis (Kala-azar): All patients  Combination: Sodium stibogluconate 20 mg /kg per day IM or IV for 17 days  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days | RR |
|  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days Alternative first line treatment is:  Sodium Stibogluconate 20 mg/kg per day for 30 days (in case paromomycin is contraindicated) In relapse or pregnancy  Liposomal amphotericin B (e.g. AmBisome) 3 mg/kg per day for 10 days In HIV+ patients  Liposomal amphotericin B 5 mg/kg per day for 8 days | RR |
| Post Kala-Azar Dermal Leishmaniasis (PKDL)  Rare in Uganda  Sodium Stibogluconate injection 20 mg/kg/day until clinical cure. Several weeks or even months of treatment are necessary | RR |
| Note Continue treatment until no parasites detected in 2 consec­ utive splenic aspirates taken 14 days apart Patients who relapse after a 1st course of treatment with Sodium stibogluconate should immediately be re- treated with Ambisome 3 mg/kg/day for 10 days |  |
```

#### Natural Language Logic (NLL)
```
IF TREATMENT is Cutaneous Leishmaniasis (all patients)  Frequently heals spontaneously but if severe or persistent, treat as for Visceral Leishmaniasis below Visceral Leishmaniasis (Kala-azar): All patients  Combination: Sodium stibogluconate 20 mg /kg per day IM or IV for 17 days  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days, THEN LOC is RR.
IF TREATMENT is  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days Alternative first line treatment is:  Sodium Stibogluconate 20 mg/kg per day for 30 days (in case paromomycin is contraindicated) In relapse or pregnancy  Liposomal amphotericin B (e.g. AmBisome) 3 mg/kg per day for 10 days In HIV+ patients  Liposomal amphotericin B 5 mg/kg per day for 8 days, THEN LOC is RR.
IF TREATMENT is Post Kala-Azar Dermal Leishmaniasis (PKDL)  Rare in Uganda  Sodium Stibogluconate injection 20 mg/kg/day until clinical cure. Several weeks or even months of treatment are necessary, THEN LOC is RR.
IF TREATMENT is Note Continue treatment until no parasites detected in 2 consec­ utive splenic aspirates taken 14 days apart Patients who relapse after a 1st course of treatment with Sodium stibogluconate should immediately be re- treated with Ambisome 3 mg/kg/day for 10 days
```

#### Clinical Context
> **Before this item** (narrative-2686): Ministry of Health Uganda, National Tuberculosis and Leprosy Programme, 2016. Tuberculosis and Leprosy Manual, 3rd Edition

Ministry of Health Uganda, Makerere Palliative Care Unit, 2014. Palliative Care Guidelines

World Health Organisation, 2010. WHO guide for Rabies Pre and Post-Exposure Prophylaxis in Humans. http://www. who.int/rabies/ PEP\_prophylaxis\_guidelines\_June10.pdf Accessed on 25/11/2016

Ministry of Health Uganda, 2013. Uganda National Infection Prevention and Control Guidelines
>

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify each weight band's dose matches WHO guidelines source PDF page 229, 230.
- [ ] **Stratification** — Confirm weight/age bands cover the full intended population; no merged or missing rows.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify that the NLL (Natural Language Logic) correctly represents the weight→dose mapping from the table.
- [ ] **Provenance** — Confirm source page 229, 230 and section 5.2.1.1.2 Dosing of ACTs match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 2. stitched_table-S1
**Pages:** 229, 230 | **Section:** 5.2.1.1.2 Dosing of ACTs
**Validation:** No validation data | **Condition:** Malaria | **Dosage:** 17 days, oral

**Audit hash:** `362a1e3e16468900...`

#### Extracted Content
```
| TREATMENT | LOC |
| --- | --- |
| Cutaneous Leishmaniasis (all patients)  Frequently heals spontaneously but if severe or persistent, treat as for Visceral Leishmaniasis below Visceral Leishmaniasis (Kala-azar): All patients  Combination: Sodium stibogluconate 20 mg /kg per day IM or IV for 17 days  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days | RR |
|  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days Alternative first line treatment is:  Sodium Stibogluconate 20 mg/kg per day for 30 days (in case paromomycin is contraindicated) In relapse or pregnancy  Liposomal amphotericin B (e.g. AmBisome) 3 mg/kg per day for 10 days In HIV+ patients  Liposomal amphotericin B 5 mg/kg per day for 8 days | RR |
| Post Kala-Azar Dermal Leishmaniasis (PKDL)  Rare in Uganda  Sodium Stibogluconate injection 20 mg/kg/day until clinical cure. Several weeks or even months of treatment are necessary | RR |
| Note Continue treatment until no parasites detected in 2 consec­ utive splenic aspirates taken 14 days apart Patients who relapse after a 1st course of treatment with Sodium stibogluconate should immediately be re- treated with Ambisome 3 mg/kg/day for 10 days |  |
```

#### Natural Language Logic (NLL)
```
IF TREATMENT is Cutaneous Leishmaniasis (all patients)  Frequently heals spontaneously but if severe or persistent, treat as for Visceral Leishmaniasis below Visceral Leishmaniasis (Kala-azar): All patients  Combination: Sodium stibogluconate 20 mg /kg per day IM or IV for 17 days  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days, THEN LOC is RR.
IF TREATMENT is  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days Alternative first line treatment is:  Sodium Stibogluconate 20 mg/kg per day for 30 days (in case paromomycin is contraindicated) In relapse or pregnancy  Liposomal amphotericin B (e.g. AmBisome) 3 mg/kg per day for 10 days In HIV+ patients  Liposomal amphotericin B 5 mg/kg per day for 8 days, THEN LOC is RR.
IF TREATMENT is Post Kala-Azar Dermal Leishmaniasis (PKDL)  Rare in Uganda  Sodium Stibogluconate injection 20 mg/kg/day until clinical cure. Several weeks or even months of treatment are necessary, THEN LOC is RR.
IF TREATMENT is Note Continue treatment until no parasites detected in 2 consec­ utive splenic aspirates taken 14 days apart Patients who relapse after a 1st course of treatment with Sodium stibogluconate should immediately be re- treated with Ambisome 3 mg/kg/day for 10 days
```

#### Clinical Context
> **Before this item** (narrative-2686): Ministry of Health Uganda, National Tuberculosis and Leprosy Programme, 2016. Tuberculosis and Leprosy Manual, 3rd Edition

Ministry of Health Uganda, Makerere Palliative Care Unit, 2014. Palliative Care Guidelines

World Health Organisation, 2010. WHO guide for Rabies Pre and Post-Exposure Prophylaxis in Humans. http://www. who.int/rabies/ PEP\_prophylaxis\_guidelines\_June10.pdf Accessed on 25/11/2016

Ministry of Health Uganda, 2013. Uganda National Infection Prevention and Control Guidelines
>

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify each weight band's dose matches WHO guidelines source PDF page 229, 230.
- [ ] **Stratification** — Confirm weight/age bands cover the full intended population; no merged or missing rows.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify that the NLL (Natural Language Logic) correctly represents the weight→dose mapping from the table.
- [ ] **Provenance** — Confirm source page 229, 230 and section 5.2.1.1.2 Dosing of ACTs match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 3. stitched_table-S1
**Pages:** 229, 230 | **Section:** 5.2.1.1.2 Dosing of ACTs
**Validation:** No validation data | **Condition:** Malaria | **Dosage:** 17 days, oral

**Audit hash:** `362a1e3e16468900...`

#### Extracted Content
```
| TREATMENT | LOC |
| --- | --- |
| Cutaneous Leishmaniasis (all patients)  Frequently heals spontaneously but if severe or persistent, treat as for Visceral Leishmaniasis below Visceral Leishmaniasis (Kala-azar): All patients  Combination: Sodium stibogluconate 20 mg /kg per day IM or IV for 17 days  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days | RR |
|  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days Alternative first line treatment is:  Sodium Stibogluconate 20 mg/kg per day for 30 days (in case paromomycin is contraindicated) In relapse or pregnancy  Liposomal amphotericin B (e.g. AmBisome) 3 mg/kg per day for 10 days In HIV+ patients  Liposomal amphotericin B 5 mg/kg per day for 8 days | RR |
| Post Kala-Azar Dermal Leishmaniasis (PKDL)  Rare in Uganda  Sodium Stibogluconate injection 20 mg/kg/day until clinical cure. Several weeks or even months of treatment are necessary | RR |
| Note Continue treatment until no parasites detected in 2 consec­ utive splenic aspirates taken 14 days apart Patients who relapse after a 1st course of treatment with Sodium stibogluconate should immediately be re- treated with Ambisome 3 mg/kg/day for 10 days |  |
```

#### Natural Language Logic (NLL)
```
IF TREATMENT is Cutaneous Leishmaniasis (all patients)  Frequently heals spontaneously but if severe or persistent, treat as for Visceral Leishmaniasis below Visceral Leishmaniasis (Kala-azar): All patients  Combination: Sodium stibogluconate 20 mg /kg per day IM or IV for 17 days  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days, THEN LOC is RR.
IF TREATMENT is  Plus paromomycin 15 mg/kg [11 mg base] per day IM for 17 days Alternative first line treatment is:  Sodium Stibogluconate 20 mg/kg per day for 30 days (in case paromomycin is contraindicated) In relapse or pregnancy  Liposomal amphotericin B (e.g. AmBisome) 3 mg/kg per day for 10 days In HIV+ patients  Liposomal amphotericin B 5 mg/kg per day for 8 days, THEN LOC is RR.
IF TREATMENT is Post Kala-Azar Dermal Leishmaniasis (PKDL)  Rare in Uganda  Sodium Stibogluconate injection 20 mg/kg/day until clinical cure. Several weeks or even months of treatment are necessary, THEN LOC is RR.
IF TREATMENT is Note Continue treatment until no parasites detected in 2 consec­ utive splenic aspirates taken 14 days apart Patients who relapse after a 1st course of treatment with Sodium stibogluconate should immediately be re- treated with Ambisome 3 mg/kg/day for 10 days
```

#### Clinical Context
> **Before this item** (narrative-2686): Ministry of Health Uganda, National Tuberculosis and Leprosy Programme, 2016. Tuberculosis and Leprosy Manual, 3rd Edition

Ministry of Health Uganda, Makerere Palliative Care Unit, 2014. Palliative Care Guidelines

World Health Organisation, 2010. WHO guide for Rabies Pre and Post-Exposure Prophylaxis in Humans. http://www. who.int/rabies/ PEP\_prophylaxis\_guidelines\_June10.pdf Accessed on 25/11/2016

Ministry of Health Uganda, 2013. Uganda National Infection Prevention and Control Guidelines
>

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify each weight band's dose matches WHO guidelines source PDF page 229, 230.
- [ ] **Stratification** — Confirm weight/age bands cover the full intended population; no merged or missing rows.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify that the NLL (Natural Language Logic) correctly represents the weight→dose mapping from the table.
- [ ] **Provenance** — Confirm source page 229, 230 and section 5.2.1.1.2 Dosing of ACTs match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

## TIER 4 — Evidence Tables + High-Priority Narratives (242 chunks) — RECOMMENDED REVIEW

> Contains clinical thresholds, dosing keywords, or contraindication information. Recommended review for additional clinical safety assurance.

### Section: Unknown section

### 4. narrative-0016
**Pages:** ? | **Section:** Contributors to the clinical chapters
**Validation:** No validation data

**Audit hash:** `f327b3119afcaaf1...`

#### Extracted Content
```
- Dr. Jacqueline Mabweijano, Consultant Surgeon Mulago NRH
- Dr. Charles Kabugo, Director / Consultant Kiruddu Hospital
- Dr. Denis Rubahika (MCP-MOH)
- Dr. Florence Christine Najjuka (Microbiology)
- Dr. Charles Mondo (Cardiovascular)
- Dr. J B Waniaye - Emergency and Trauma
- Dr. John.O. Omagino (Cardiovascular)
- Dr. William Worodria, Senior Consultant, Mulago NRH
- Dr. Kalani SMO-MOH,
- Dr. Francis Lakor, Consultant, maxilla facial surgery Mulago NRH
- Dr. Dhabangi consultant haematology - Blood transfusion Mulago NRH
- Dr. Christine Sekaggya-Wiltshire, Physician-Hematologist, Mulago NRH
- Dr. Henry Ddungu, Physician-Hematologist, UCI
- Mr. Lule Albert, PNO- Mulago NRH
- Dr. Patrick Musinguzi, Consultant, Mulago NRH
- Dr. Abubaker Bugembe, Consultant, Mulago NRH
- Dr. Jackson Orem, Director, Uganda Cancer Institute
- Mr. Rodney Tabaruka, Pharmacist Kabale RRH
- Mr. Emmanuel Ongom, Medical Clinical Officer, Gulu RRH
- Ms. Martha Ajulong, (ACHS, Pharmacy)
- Ms. Harriet Akello, Senior Pharmacist MOH
- Mr. Gad Twikirize, Senior Pharmacist, Butabika NRH
- Dr. Fualal Jane Odubu, Sen.Cons. -Mulago NRH,
- Dr. Kajumbula Henry- S/Lecturer, MAK CHS,
- Dr. Munube Deogratias, Consultant Paed-MNRH,
- Ms. Atim Mary Gorret - Sen. Pharm-KNRH
- Dr. Namagembe Imelda, Sen. Cons.- MNRH
- Dr. Amone Jackson CHS(CS)-MOH
- Dr. Wasomoka Alex ACHS - HLLHF -MOH
- Dr. Namubiru Saudah Kizito, Clinical Microbiologist, MOH/NHLDS
- Dr. Bahatungire Rony, PMO/CS -MOH
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify Level of Care assignments (HOSPITAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section Contributors to the clinical chapters match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 5. narrative-0037
**Pages:** ? | **Section:** New Feature
**Validation:** No validation data

**Audit hash:** `4d64e8299d18d3e2...`

#### Extracted Content
```
The chapters Covid -19, Self-care and Hypoxia management have been added with focus on primary care (prevention and early recognition of symptoms).

Disease monographs are organized in the order of: definition, cause/ risk factors, clinical features and complications, differential diagnosis, investigations, management, and prevention.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section New Feature match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 6. narrative-0038
**Pages:** ? | **Section:** New Feature
**Validation:** No validation data

**Audit hash:** `9115beb51c36c5ac...`

#### Extracted Content
```
Palliative care ladder has been introduced to make it easier for pain assessment. Treatments are presented in logical order from non-pharmacological to

pharmacological, from the lower to the higher level of care. Where possible, alternatives and second-line options have been presented, as well as referral criteria.

Medicines are presented by their generic name, in bold. Unless otherwise specified, dosages are for adults and via oral route. Children's dosages are added whenever indicated, as well as duration and other instructions.

The level of care (LOC) is an important feature; it provides information about the level at which the condition can be appropriately managed. Often, treatment can be initiated at lower level, but the patient needs to be referred for further management, or for second-line treatment, or for complications. For antibiotics, it is recommended that treatment can be initiated in some cases awaiting laboratory results. HC1-4 refers to health centres of different levels (with HC1 being the community level), H to general hospital, RR to regional referralhospital, and NR to national referralhospital.

After familiarizing yourself with it, try using it! Practice finding conditions and looking them up to see how they are managed, using either the table of contents at the beginning or the index at the end.

Read all the introductory sections. They will give you useful advice for your daily practice. There is always something new to learn or to be reminded of.

Use it in your daily practice. The UCG is designed as a simple reference manual to keep at your work station, where you can consult it any time. Using it in front of patients and colleagues will show that you care deeply about the quality of your work, and it will provide good examples to other health workers.

The UCG cannot replace health workers'knowledge and skills; like your thermometer and stethoscope, it is a tool to help improve clinical practice by providinga quick and easily available summary of the recommended management of common health conditions.
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify Level of Care assignments (HEALTHCENTRE, HOSPITAL, NATIONALREFERRAL, REGIONALREFERRAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section New Feature match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 7. narrative-0040
**Pages:** ? | **Section:** What has changed compared to the previous edition?
**Validation:** No validation data

**Audit hash:** `5f78cf990c0a5ddb...`

#### Extracted Content
```
- ~ There are more chapters as explained before.
- ~ The management sections have been re-edited to be more user-friendly, using the suggestions collected during a user survey.
- ~ Information on new diseases has been added, following new epidemics and public health priorities (e.g., viral haemorrhagic fevers, Covid-19, yellow fever, nodding disease, sickle cell disease, newborn illnesses).
- ~ More attention has been paid to non-communicable chronic diseases; for example, stroke and chronic obstructive pulmonary disease (COPD), and sections on diabetes, hypertension, asthma and mental conditions including diseases of elderly and dementia have been expanded.
- ~ Recommendations have been aligned with the most recent national and international guidelines related to ART, TB, malaria, IMNCI, IMPAC, mhGAP (see the list of references in Appendix 4).
- ~ Medications have been added or deleted and level of care has changed according to recent evidence and national policies.
- ~ Skin management of Albinos using a sunscreen protection product has been included under the dermatological section.
- ~ The essential medicines list has been removed from this edition to make the book pocket friendly.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section What has changed compared to the previous edition? match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 8. narrative-0042
**Pages:** ? | **Section:** What about the Essential Medicines and Health Supply List (EMHSLU)?
**Validation:** No validation data

**Audit hash:** `6f939f5deaa18b39...`

#### Extracted Content
```
The EMHSLU has all the medicines recommended in the UCG, with specification of the level of care (LOC) at which they can start being used, but it also has additional "specialty" medicines, which are items used at referral level (regional or national) or in the context of specialized services. TheymaynotbeincludedintheUCG,whichfocus more on primary care, but are still part of the list because they need to be procured to ensure the provision of a wider range of services at secondary and tertiary levels. In the context of limited resources, it is very important to learn to prioritize medicines for procurement:this is reflected by the vital, essential, necessary (VEN) classification in the EMHSLU, introduced in 2012.

Uganda Clinical Guidelines 2023

XLIX

Uganda Clinical Guidelines 2023

L

Medicines are classified into three categories according to health impact:

V: vital medicines are potentially life-saving, and lack of availability would cause serious harm and side effects. These must ALWAYS be available-for example insulin, metformin, most antibiotics, first-line antimalarials, some anti-epileptics, and parenteral diuretics.

E: essential medicines are important; they are used to treat common illnesses that are maybe less severe but still significant. They are not absolutely needed for the provision of basic health care (e.g., anti-helminthics, pain killers).

N: necessary (or sometimes called non-essential) medicines are used for minor or self-limiting illnesses, or may have a limited efficacy, or a higher cost compared to the benefit.

Everyefforthastobemadetoensurehealthfacilitiesdonot suffer stock-outs of VITAL MEDICINES.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section What about the Essential Medicines and Health Supply List (EMHSLU)? match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 9. narrative-0054
**Pages:** ? | **Section:** Appropriate Medicines Use
**Validation:** No validation data

**Audit hash:** `09da5542c4d1826c...`

#### Extracted Content
```
According to WHO, "Rational [appropriate] use of medicines requires that patients receive medications appropriate to their clinical needs, in doses that meet their ownindividual requirements, for an adequate period of time, and at the lowest cost to them and their community".

Inappropriate medicine use can not only harm the patient, but by wasting resources, may limit the possibility of other people accessing healthcare! Both health workersand patients havean important role to play in ensuring appropriate use by:

- ~ Prescribing (and taking) medicines ONLY when they are needed
- ~ Avoiding giving unnecessary multiple medications to satisfy patients' demands or for financial gain

Uganda Clinical Guidelines 2023

LV

Uganda Clinical Guidelines 2023

LV I

- ~ Avoiding expensive alternative or second-line medications when an effective and inexpensive first-line is available
- ~ Avoiding injections when oral treatment is perfectly adequate
- ~ Ensuring that the correct dose and duration of treatment is prescribed, especially for antibiotics, to avoid resistance
- ~ Providing adequate information and counselling to the patient to ensure adherence with instructions.
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section Appropriate Medicines Use match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 10. narrative-0055
**Pages:** ? | **Section:** According to the WHO definition
**Validation:** No validation data

**Audit hash:** `03c582c43628494e...`

#### Extracted Content
```
"Antimicrobial resistance occurs when microorganisms such as bacteria, viruses, fungi and parasites change in ways that render the medications used to cure the infections they cause ineffective. Antimicrobial resistance is facilitated by the inappropriate use of medicines, for example, when taking substandard doses or not finishing a prescribed course of treatment. Low-qualitymedicines, wrong prescriptions and poor infection prevention and control also encourage the developmentandspreadofdrugresistance".

The problem of AMR is a serious threat for the modern world:

- ~ The resistance of malaria parasites has caused several changes in antimalarial regimens in the last 15 years
- ~ MDR-TB (multi-drug resistant tuberculosis) is spreading and requires long and complex treatments
- ~ HIV resistance is a serious concern, especially after longterm treatment
- ~ AMR is spreading and, in some cases, commonly used antimicrobials are not as effective as before
- ~ Antimicrobial resistance amomg bacteria other than TB and fungi (moulds and yeasts) that affect the immune-compromised is evolving, spreading and responsible for death from sepsis in general and high dependency units.

Inappropriae use of antibiotics (in human medicine but also in animal agriculture), poor quality products and ineffective infection control measures are all contributing factors. We are seriously at risk of finding ourselves in a situation with no affordable antimicrobial available to cure common and dangerous infections.

It is URGENT that both health workers and patients become aware of the problem and start acting by:

- ~ Using antimicrobials only when it is really necessary and according to recommendations (e.g. not for simple viral infections!)
- ~ Avoiding self-prescription of antibiotics
- ~ Avoiding using last generation and broad spectrum antibiotics as first-line treatment
- ~ Prescribing correct dosages for the correct duration and ensuring adherence to the prescription
- ~ Practising strict measures of infection control in health facilities
- ~ Improving hygiene and sanitation in the community, thereby reducing the circulation of germs.
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section According to the WHO definition match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 11. narrative-0059
**Pages:** ? | **Section:** Prescribing placebos
**Validation:** No validation data

**Audit hash:** `94336e7e53ecd1d3...`

#### Extracted Content
```
Avoid placebos whenever possible. Instead, spend some time reassuring and educating the patient. Use home remedies when possible (e.g., honey for cough in adults and children above 1 year).
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section Prescribing placebos match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 12. narrative-0060
**Pages:** ? | **Section:** Prescription writing
**Validation:** No validation data

**Audit hash:** `11761589ed8a6968...`

#### Extracted Content
```
A wrong prescription is very risky for you and your patient.

Unclear, incomplete, or inaccurate prescriptions are very dangerous for the patient. To avoid problems, follow the guidance below in writing your prescriptions:
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section Prescription writing match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 13. narrative-0063
**Pages:** ? | **Section:** PRESCRIPTION WRITING RULES
**Validation:** No validation data

**Audit hash:** `5f5e358600a30ea0...`

#### Extracted Content
```
- ~ Write the full name, age, gender and address of the patient, then sign and date the prescription form
- ~ All prescriptions should clearly indicate the name and address of the prescriber and of the facility
- ~ A PRESCRIPTION IS A LEGAL DOCUMENT
- ~ Write the name of the medicine or preparation using its full generic name.
- ~ Unofficial abbreviations, trade names, and obsolete names should not be used.
- ~ State the strength of the medicine prescribed where relevant:
- ~ Quantities of one gram or more should be written as 1g, 2.5g, 10g, and so on
- ~ Quantities &lt;1g but &gt;1mg should be expressed in milligrams rather than grams, for example, 500mg and not 0.5g
- ~ Quantities &lt;1mg should be expressed in micrograms and not in mg, for example, 100 micrograms rather than 0.1 mg or 100 mcg
- ~ If decimal figures are used, always write a zero in front of the decimal point where there is no other figure, for example 0.5 ml and not .5 ml
- ~ Always state dose regimen in full:
- -Dose size, Dose frequency, Duration of treatment
- ~ The quantity to be dispensed is calculated from the regimen.
- ~ F or example, doxycycline 100 mg every 12 hours for 7 days = to be dispensed: 14 tablets of 100 mg.
- ~ For in-patients, clearly state the route of administration and specify time of administration, if relevant

Uganda Clinical Guidelines 2023

LXI

Uganda Clinical Guidelines 2023

LXII
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section PRESCRIPTION WRITING RULES match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 14. narrative-0064
**Pages:** ? | **Section:** PRESCRIPTION WRITING RULES
**Validation:** No validation data

**Audit hash:** `b9059a15e1a6a8c8...`

#### Extracted Content
```
- ~ Avoid use of instructions like "prn" or "to be used/taken as required".Indicatea suitable dose frequency instead
- ~ In the few cases where "as required" is appropriate, always state the actual quantity of the medicine to be supplied, when to take it and maximum amount
- ~ Where relevant, always remember to include on the prescription any special instructions necessary for the correct use of a medicine or preparation,for example "before food" or "apply sparingly".
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section PRESCRIPTION WRITING RULES match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 15. narrative-0067
**Pages:** ? | **Section:** Prescribing in children and the elderly
**Validation:** No validation data

**Audit hash:** `07d6f9d8c4b776b0...`

#### Extracted Content
```
In these guidelines, paediatric medicine doses are usually givenaccording to body weightand not age, and are therefore expressed as mg/kg.

The main reason for this is that children of the same age may vary significantly in weight. Thus, it is safer and more accurate to prescribe medicines according to body weight. Moreover, this should encourage the good practice of weighing children whenever possible.

Uganda Clinical Guidelines 2023

LXIII

Uganda Clinical Guidelines 2023

LXIV

However,as a guide to prescribing by weightwhen a weighing scale is not available, the weight-for-age charts at the end of Chapter 17 can be used as an estimate for children from 1-24 months and 2-15 years, respectively. Always use lean/ideal body weight for children who are overweight/obese to avoid giving them overdoses.
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section Prescribing in children and the elderly match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 16. narrative-0069
**Pages:** ? | **Section:** Medicine interactions
**Validation:** No validation data

**Audit hash:** `1803ee9024b7f233...`

#### Extracted Content
```
Before prescribing anymedicine, take care to avoidproblems of interactions with other medicines by obtaining details of any other medication that the patient is taking, whether the medication is:

- ~ Also prescribed at the same time
- ~ Previously prescribed by another prescriber for the same or another condition and currentlybeing taken by the patient
- ~ Purchased or otherwise obtained by the patient for thepurposes of self-medication at home.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section Medicine interactions match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 17. narrative-0070
**Pages:** ? | **Section:** Medicine interactions
**Validation:** No validation data

**Audit hash:** `55e9710a86745976...`

#### Extracted Content
```
Note on interactions with alcohol. If a prescribed medicine interacts with alcohol (for example, metronidazole, diazepam, anti-diabetic medicines, and tricyclic antidepressants), caution the patient to avoidtaking alcoholic drinks during the course of treatment and for 48 hours afterwards.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section Medicine interactions match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 18. narrative-0071
**Pages:** ? | **Section:** Patient counselling
**Validation:** No validation data

**Audit hash:** `2f361aecc44df1b0...`

#### Extracted Content
```
This vital part of patient management is often neglected with potentially serious consequences. Although counselling the patient may take time, if done systematically, it should only take a few minutes and could make the difference between treatment success and failure.

Include the followingkeycomponents when counselling the patient:

- ~ Explain the diagnosis and the likely cause of the disease or condition and discuss the proposed approach to treatment
- ~ Describe the prescribed medicine therapy in detail including:
-  Medicine name
-  Function of the medicine
-  Dose regimen (size, frequency, duration)
-  Any additional instructions on correct use or storage of the medicine

Uganda Clinical Guidelines 2023

LXV

Uganda Clinical Guidelines 2023

LXVI

-  Any likely side effects and what to do if they occur
-  Advise on important medicine interactions (including with alcohol)
- ~ Give advice on how to contribute to the success of the treatment (for example, rest, diet, fluids and other lifestyle changes) and how to avoid the same problem in future
- ~ Ensure the patient or caretaker fully understands the information and advice provided-ask him or her to repeat key points
- ~ For health conditions that require self-care, proper advice should be given to the patient on self-awareness, self-testing and self-management.
-  Ensure the patient is satisfied with the proposed treatment and has an opportunity to raise any problems or queries with you.

1
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section Patient counselling match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.1 COMMON EMERGENCIES > 1.1.1 Anaphylactic Shock

### 19. narrative-0077
**Pages:** ? | **Section:** 1.1.1 Prevention
**Validation:** No validation data

**Audit hash:** `a49bf8dde9c9d0d0...`

#### Extracted Content
```
- ~ Always ask about allergies before giving patients new medicine
- ~ Keep emergency drugs at hand at health facilities and in situatiuons where risk of anaphlaxis is high, e.g. visiting bee hives or places that usually harbour snakes
- ~ Counsel allergic patients to wear alert bracelet or tag.
```

#### Extracted Clinical Flags
- **Special populations:** hives or places that usually harbour snakes
- ~ Counsel allergic patients to wear alert bracelet or 

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 1.1.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.1 COMMON EMERGENCIES > 1.1.2 Hypovolaemic Shock ICD10 CODE: R57.1

### 20. narrative-0083
**Pages:** ? | **Section:** 1.1.2 If established hypovolaemia class 2 and above
**Validation:** No validation data

**Audit hash:** `3217995bae7e5c3b...`

#### Extracted Content
```
-  Set 2 large bore IV lines
- IV fluids Normal Saline 0.9% (or Ringer's lactate ) 2030 ml/kg over60 minutes according to response
- -If possible, warm the fluid
- -Start rapidly, monitor BP
- -Assess response to fluid resuscitation: BP, HR, RR, capillary refill, consciousness and urinary output



If internal or external haemorrhage, consider blood transfusion

If rapid improvement and stable (blood loss &lt;20% and not progressing)

- [ ]  Slow IV fluids to maintenance levels



No immediatetransfusion but do cross-matching

-  Regular reassessment

- [ ]  Detailed examination and definitive treatment according to the caus e

If transient improvement (blood loss 20-40% or ongoing bleeding)

- [ ]  Rapid administration of fluids

- [ ]  Initiate blood transfusion (see section 11.2)

-  Regular reassessment

- [ ]  Detailed examination and early surgery

If no improvement

-  Vigorous fluid administration
-  Urgent blood transfusion



Immediate surgery

LOC

HC3

HC4

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

5

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

6
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.1.2 If established hypovolaemia class 2 and above match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.1 COMMON EMERGENCIES > 1.1.3 Dehydration > 1.1.3.2 Dehydration in Older Children and Adults

### 21. narrative-0095
**Pages:** ? | **Section:** 1.1.3.2 Management
**Validation:** No validation data

**Audit hash:** `04e2b669ba7f3dfb...`

#### Extracted Content
```
-  After 4 hours, evaluate rehydration in terms of clinical signs (NOT in terms of volumes of fluid given)
-  As soon as signs of dehydration have disappeared (but not before), start fluid maintenance therapy, alternating ORS and water (to avoid hypernatraemia) as much as the patient wants

Continue for as long as the cause of the original dehydration persists.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.1.3.2 Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 22. narrative-0097
**Pages:** ? | **Section:** 1.1.3.2 Caution
**Validation:** No validation data

**Audit hash:** `bb3191df3dfb7a6c...`

#### Extracted Content
```
-  Avoid artificially sweetened juices.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.1.3.2 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.1 COMMON EMERGENCIES > 1.1.6 Hypoglycaemia ICD10 CODE: E16.2

### 23. narrative-0127
**Pages:** ? | **Section:** 1.1.6 Note
**Validation:** No validation data

**Audit hash:** `d8e9827e5b43b459...`

#### Extracted Content
```
-  After dextrose 50%, flush the IV line to avoid sclerosis of the vein (dextrose is very irritant)
-  Preparation of Dextrose 10% from Dextrose 5% and Dextrose 50%:
- -Remove 50 ml from Dextrose 5% bottle and discard
- -Replace with 50 ml of Dextrose 50%. Shake
- -Follow normal aseptic techniques
- -Use immediately, DO NOT STORE.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.1.6 Note match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 24. narrative-0128
**Pages:** ? | **Section:** 1.1.6 Prevention
**Validation:** No validation data

**Audit hash:** `7c8387d0cd0a2374...`

#### Extracted Content
```
- ~ Educate patients at risk of hypoglycaemia on recognition of early symptoms e.g. diabetics, patients who have had a gastrectomy
- ~ Advise patients at risk to have regular meals and to always have glucose or sugar with them for emergency treatment of hypoglycaemia
- ~ Advise diabetic patients to carry an identification tag
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 1.1.6 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.2 TRAUMA AND INJURIES > 1.2.1 Bites and Stings > 1.2.1.1 Snakebites

### 25. narrative-0139
**Pages:** ? | **Section:** 1.2.1.1 Investigations
**Validation:** No validation data

**Audit hash:** `86f15e7b0b0e8e4e...`

#### Extracted Content
```
- ~ Whole blood clotting test at arrival and every 4-6 hours after the first day:
-  Put 2-5 ml of blood in a dry tubeand observe after 30 minutes
-  If incomplete or no clotting, it indicates coagulation abnormalities
- ~ Other useful tests depending on severity, level of care and availability:
-  Oxygen Saturation/PR/BP/RR
-  Haemoglobin/PCV/Platelet count/PT/APTT/D-Dimer
-  Biochemistry for Serum Creatinine/Urea/Potassium
-  Urine Tests for Proteinuria/Haemoglobinuria/ Myoglobinuria
-  Imaging ECG/X-Ray/Ultrasound

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

29

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

30
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.2.1.1 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.2 TRAUMA AND INJURIES > 1.2.1 Bites and Stings > 1.2.1.5 Rabies Vaccine Schedules

### 26. narrative-0185
**Pages:** ? | **Section:** 1.2.1.5 Management
**Validation:** No validation data

**Audit hash:** `3945f365ef77ebcc...`

#### Extracted Content
```
Suspected fractures should be referred to HC4 or Hospital after initial care.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify Level of Care assignments (HC4, HOSPITAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 1.2.1.5 Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 27. narrative-0187
**Pages:** ? | **Section:** 1.2.1.5 Caution
**Validation:** No validation data

**Audit hash:** `5a3aeff4fa3e6166...`

#### Extracted Content
```
-  Do not give pethidine and morphine for rib fractures and head injuries as they cause respiratory depression

1.2.3 Burns
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.2.1.5 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 28. narrative-0190
**Pages:** ? | **Section:** 1.2.1.5 Clinical features
**Validation:** No validation data

**Audit hash:** `339cc2a9844c7ca8...`

#### Extracted Content
```
- ~ Pain, swelling
- ~ Skin changes (hyperaemia, blisters, singed hairs)
- ~ Skin loss (eschar formation, charring)
- ~ Reduced ability to use the affected part
- ~ Systemic effects in severe/extensive burns include shock, low urine output, generalised swelling, respiratory insufficiency, deteriorated mental state
- ~ Breathing difficulty, hoarse voice and cough in smoke inhalation injury - medical emergency
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 1.2.1.5 Clinical features match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 29. narrative-0199
**Pages:** ? | **Section:** 1.2.1.5 Prevention
**Validation:** No validation data

**Audit hash:** `3e163e24fc4326a5...`

#### Extracted Content
```
- ~ Public awareness of burn risks and first aid water use in cooling burnt skin
- ~ Construction of raised cooking fire places as safety measure
- ~ Ensure safe handling of hot water and food, keep well out of the reach of children
- ~ Particular care of high risk persons near fires e.g. children, epileptic patients, alcohol or drug abusers
- ~ Encourage people to use closed flames e.g. hurricane lamps. Avoid candles.
- ~ Beware of possible cases of child abuse
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.2.1.5 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.2 TRAUMA AND INJURIES > 1.2.5 Head Injuries

### 30. narrative-0213
**Pages:** ? | **Section:** 1.2.5 Management (general principles)
**Validation:** No validation data

**Audit hash:** `b79a5a6a33dc280e...`

#### Extracted Content
```
Management depends on:

- ~ GCS and clinical features at first assessment
- ~ Risk factors (mechanism of trauma, age, baseline conditions)
- ~ GCS and clinical features at follow up
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.2.5 Management (general principles) match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 31. narrative-0214
**Pages:** ? | **Section:** 1.2.5 Prevention
**Validation:** No validation data

**Audit hash:** `168892c923f1658c...`

#### Extracted Content
```
- ~ Careful (defensive) driving to avoid accidents
- ~ Use of safety belts by motorists
- ~ Wearing of helmets by cyclists, motor-cyclists and people working in hazardous environments
- ~ Avoid dangerous activities (e.g., climbing trees)
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.2.5 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.2 TRAUMA AND INJURIES > 1.2.6 Sexual Assault/Rape

### 32. narrative-0218
**Pages:** ? | **Section:** 1.2.6 Management of mild traumatic head injury
**Validation:** No validation data

**Audit hash:** `1e216dcdddead583...`

#### Extracted Content
```
- ~ Extragenital injury
- ~ Genital injury (usually minor, but some vaginal lacerations can be severe)
- ~ Psychologic symptoms: often the most prominent
- -Short term: fear, nightmares, sleep problems, anger, embarrassment
- -Long term: Post traumatic Stress Disorder, an anxiety
- -disorder; symptoms include re-experiencing (e.g., flashbacks, intrusive upsetting thoughts or images), avoidance (e.g., of trauma-related situations, thoughts, and feelings) and hyperarousal (e.g., sleep difficulties, irritability, concentration problems).
- -Symptoms last for &gt;1 month and significantly impair social and occupational functioning.
- -Shame, guilt or a combination of both
- -Sexually transmitted infections (STIs, e.g., hepatitis, syphilis, gonorrhea, chlamydial infection, trichomoniasis, HIV infection)
- ~ Pregnancy (may occur)
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 1.2.6 Management of mild traumatic head injury match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.3 POISONING > 1.3.3 Paraffin and Other Petroleum Products Poisoning ICD10 CODE: T53.7

### 33. narrative-0241
**Pages:** ? | **Section:** 1.3.3 Clinical features
**Validation:** No validation data

**Audit hash:** `0975993b1cafb857...`

#### Extracted Content
```
- ~ Patient may smell of paraffin/other petroleum product
- ~ Burning sensation in mouth and throat
- ~ Patient looks pale (transient cyanosis)
- ~ Vomiting, diarrhoea, bloody stools
- ~ Cough, dyspnoea, wheezing, tachypnoea, nasal flaring (due to chemical pneumonitis)
- ~ Lethargy, convulsions, difficulty in breathing

The main risk is damage to lung tissue due to aspiration. AVOID gastric lavage or use of emetics as this may lead to inhalation of gastric content and pneumonitis
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.3.3 Clinical features match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 34. narrative-0244
**Pages:** ? | **Section:** 1.3.3 Child: 0.05 mg/kg per dose
**Validation:** No validation data

**Audit hash:** `140fdd7d69947fac...`

#### Extracted Content
```
- -Continuous infusion of atropine 0.05 mg/kg/
- -Double dose every 3-5 minutes until signs of atropinisation occur (stopping of bronchial secretions and broncoconstrictions)
- hour may be necessary
- -
- Reduce dose of atropine slowly over 24 hours but monitor for patient's status

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

73

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

74

- ~ Store paraffin and other petroleum products safely (e.g. in a locked cupboard, out of reach of children)
- ~ Do not store paraffin and other petroleum products in common beverage bottles.
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.3.3 Child: 0.05 mg/kg per dose match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.3 POISONING > 1.3.5 Paracetamol Poisoning ICD10 CODE: T39.1

### 35. narrative-0247
**Pages:** ? | **Section:** 1.3.5 Paracetamol Poisoning ICD10 CODE: T39.1
**Validation:** No validation data

**Audit hash:** `2ffe96818b379d32...`

#### Extracted Content
```
Accidental or intentional assumption of excessive amount of paracetamol. Toxic dose: &gt;150 mg/kg or &gt;7.5 g (200 mg/kg for children &lt;6 years)
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.3.5 Paracetamol Poisoning ICD10 CODE: T39.1 match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.3 POISONING > 1.3.6 Iron Poisoning ICD10 CODE: T45.4

### 36. narrative-0251
**Pages:** ? | **Section:** 1.3.6 Iron Poisoning ICD10 CODE: T45.4
**Validation:** No validation data

**Audit hash:** `1fe49b9aea3409d7...`

#### Extracted Content
```
Common in children, due to the candy-like aspect of iron tablets. Ingestion of a quantity &lt;40 mg/kg of elemental iron is unlikely to cause problems. Doses &gt;60 mg/kg can cause serious toxicity.

Note: the common tablet of 200 mg of an iron salt contains 60-65 mg of elemental iron.
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.3.6 Iron Poisoning ICD10 CODE: T45.4 match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.3 POISONING > 1.3.13 Food Poisoning ICD10 CODE: A05

### 37. narrative-0288
**Pages:** ? | **Section:** 1.3.13 Prevention
**Validation:** No validation data

**Audit hash:** `516dffcb0d309a0e...`

#### Extracted Content
```
- ~ Heat cooked foods thoroughly before eating and avoid eating cold left-over cooked foods
- ~ Ensure adequate personal and domestic hygiene
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 1.3.13 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 1.4 HYPOXEAMIA MANAGEMENT AND OXYGEN THERAPY GUIDELINES

### 38. narrative-0289
**Pages:** ? | **Section:** 1.4 HYPOXEAMIA MANAGEMENT AND OXYGEN THERAPY GUIDELINES
**Validation:** No validation data

**Audit hash:** `2f869bc8fb311e11...`

#### Extracted Content
```
Hypoxaemia is the low concentration of Oxygen in blood or oxygen saturation (SpO2) less than 90% in peripheral arterial blood detected on pulse oximeter reading. Hypoxaemia is a life-threatening condition correlated with disease severity and an emergency stat. Left untreated and for prolonged periods of time, it results into low tissue oxygen concentration (Hypoxia), and this leads to death.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 1.4 HYPOXEAMIA MANAGEMENT AND OXYGEN THERAPY GUIDELINES match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 39. narrative-0294
**Pages:** ? | **Section:** 1.4 Management
**Validation:** No validation data

**Audit hash:** `026d126da051b94a...`

#### Extracted Content
```
- ~ Pulse oximetry use. Always refer to the manufacturer's insert or the steps outlined below for guidance on how to use the pulse oximetera.
- ~ The steps involved in conducting pulse-oximetry
-  Turn on the Pulse oximeter.
-  Attach the Oximeter probe to the finger or toe.
-  Wait until there is a consistent pulse -wave signal before you take the reading, this may take 20-30 seconds.
-  Record the reading and act accordingly.
- ~ Interpreting pulse-oximetry results
-  SpO2 &gt; 90% without danger signs = Normal
-  SpO2 &lt; 90% =Low oxygen concentration in blood (Hypoxaemia)
-  SpO2 &lt;92- 95% in Pregnancy = Low oxygen concentration in blood (Hypoxaemia)
-  SpO2 &lt; 94 % with danger signs = Low oxygen concentration in blood (Hypoxaemia

Blood gas analysis-direct measurement of the partial pressure of oxygen (Pao2) and Carbon dioxide (PC02) 2, the PH and electrolytes concentration in blood. It is the most accurate, but it is highly skill dependant, expensive and invasive.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 1.4 Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 40. narrative-0296
**Pages:** ? | **Section:** 1.4 Indications
**Validation:** No validation data

**Audit hash:** `43f6941def93f947...`

#### Extracted Content
```
- ~ All patients with documented Hypoxaemia-arterial Carbondioxide tension (Paco2) of &lt; 60 mmHg or peripheral arterial oxygen saturation (SpO2) OF &lt; 90%.

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

89

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

90

- ~ Patients with the following danger/emergency signs irrespective of the documented SpO2, PaCO2.
- ~ Absent or obstructed breathing, Features of severe respiratory distress, Central cyanosis, Convulsions, Signs of shock, Coma
- ~ All acute conditions in which Coma is suspected like:
- ~ Acute Asthma, Severe Trauma, Acute myocardial Infarction, Carbon monoxide poisoning
- ~ Post anaesthesia recovery.
- ~ Increased metabolic demand
- ~ Severe burns, Poisoning, Multiple injuries, Severe infections
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 1.4 Indications match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 41. narrative-0302
**Pages:** ? | **Section:** 1.4 Medical Oxygen dosing and appropriate use of delivery device.
**Validation:** No validation data

**Audit hash:** `762c2a10b50c9ef4...`

#### Extracted Content
```
Worsening respiratory distress with SpO2&lt;90%

Continue to try to find a higher level of care and consider one of the following if available and adequate O2 supply: HFNO: 30-60 LPM (may also adjust FiO2)| CPAP: 10-15 cmH20 BIPAP: PS (ΔP) 5-15/PEEP (EPAP) 5-15

- ~ Weaning patient off oxygen
-  The oxygen flowrate/ dose should be decreased if patient stabilizes or improves with SpO2 above 90%.
-  Decrease oxygen flow by 1-2Litre/min once patient is stable with Oxygen saturation above 92%.
-  Observe the patient for 2-3 minutes, reassess after 15 mins to ensure Sp02 is still above 90% (by recording clinical exam and SpO2)
-  If a patient does not tolerate less oxygen, then maintain the flow rate that the patient has been on prior to reducing until the patient is stable (Sp02 &gt;92%)
-  If a patient is in increased respiratory distress or Sp02 less than 90%, then increased the oxygen flow rate to the previous rate until the patient is stable.
-  If a patient remains stable after 15 mins of reassessment and Sp02 &gt;92%, continue to titrate oxygen down as tolerated.

Recheck clinical status and Sp02 on the patient after 1 hour for delayed hypoxemia or respiratory distress.

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

93

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

94
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 1.4 Medical Oxygen dosing and appropriate use of delivery device. match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.1 BACTERIAL INFECTIONS > 2.1.4 Leprosy/Hansens disease ICD10 CODE: A30.0

### 42. narrative-0326
**Pages:** ? | **Section:** 2.1.4 Investigations
**Validation:** No validation data

**Audit hash:** `21f45af9b98a99db...`

#### Extracted Content
```
- ¾ In most cases, a definite diagnosis of leprosy can be made using clinical signs alone
- ¾ At referral centre: stain slit skin smears for Acid Fast Bacilli (AFB)
- ¾ Skin biopsies NOT recommended as a routine procedure
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 2.1.4 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 43. narrative-0335
**Pages:** ? | **Section:** 2.1.4 Management of Disability in the hand and feet
**Validation:** No validation data

**Audit hash:** `e9103262488371c2...`

#### Extracted Content
```
Resting of the affected limb in the acute phase can be aided by splinting, especially at night

- ~ Soaking and oiling for about 30 minutes every day of dry skin helps to prevent cracking and preserves the integrity of the epidermis.
- ~ Use of a clean dry cloth to cover the wounds and walking as little as possible and walk slowly, taking frequent rest. Passive exercise and stretching to avoid contractures and strengthen muscle weakness
- ~ Use of a rough stone to smoothen the skin on the feet or palms,
- ~ Protective foot wear (MCR Sandals) al, the time. For insensitive feet and protective appliances like gloves for insensitive hands
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.1.4 Management of Disability in the hand and feet match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.1 BACTERIAL INFECTIONS > 2.1.5 Meningitis

### 44. narrative-0345
**Pages:** ? | **Section:** 2.1.5 Prevention
**Validation:** No validation data | **Condition:** Meningitis

**Audit hash:** `be3569eb7e87630c...`

#### Extracted Content
```
- ~ Avoid overcrowding
- ~ Improve sanitation and nutrition
- ~ Prompt treatment of primary infection (e.g. in respiratory tract)
- ~ Immunisation as per national schedules
- ~ Mass immunisation if N. Meningitis epidemic
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.1.5 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.1 BACTERIAL INFECTIONS > 2.1.7 Septicaemia ICD10 CODE: A41.9 > 2.1.7.2 Septic Shock Management, In Adults

### 45. narrative-0368
**Pages:** ? | **Section:** 2.1.7.2 2. At ICU, Intubation and Mechanical Ventilation.
**Validation:** No validation data

**Audit hash:** `c4f994e107e94bfa...`

#### Extracted Content
```
-  The recommended tidal volume is kept at 6ml/Kg, with plateau pressure kept at or below 30ml of water.
-  Iv vasopressor Norepinephrine; 5-20µg/min.
-  Second line is synthetic human angiotensin ii,
-  or vasopressin CVP; ≤8mmHg
-  Ionotropic therapy and Augumented oxygen therapy
-  Dobutamine up to 20µg/kg/ml
-  Corticosteroids Therapy:
-  Iv hydrocortisne200mg/Kg/day in 4 divided dosages,
-  Maintenance infusion of methyl prednisolone 1mg/kg/day for 7 days, then tapper down for at least another 7 days.
-  Glycemic control Maintain glycemic level below 180mg/dl through insulin therapy
-  Deep Venous Thrombosis prophylaxis
-  UFH 2 or 3 times a day and LMWH
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.1.7.2 2. At ICU, Intubation and Mechanical Ventilation. match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.2 FUNGAL INFECTIONS > 2.2.1 Candidiasis

### 46. narrative-0400
**Pages:** ? | **Section:** 2.2.1 Prevention
**Validation:** No validation data

**Audit hash:** `413e83a3705bbd30...`

#### Extracted Content
```
- ~ Early detection and treatment
- ~ Improve personal hygiene
- ~ Avoid unnecessary antibiotics
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.2.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.3 VIRAL INFECTIONS > 2.3.2 Chicken pox ICD10 CODE: B01

### 47. narrative-0413
**Pages:** ? | **Section:** 2.3.2 Management
**Validation:** No validation data

**Audit hash:** `1ebd86624b3d6b49...`

#### Extracted Content
```
- ~ Isolation of infected patient
- ~ Avoid contact between infected persons and immuno- suppressed persons
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.3.2 Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.3 VIRAL INFECTIONS > 2.3.3 Measles ICD10 CODE: B05

### 48. narrative-0421
**Pages:** ? | **Section:** 2.3.3 Prevention
**Validation:** No validation data | **Condition:** Measles

**Audit hash:** `298fac11b66079ad...`

#### Extracted Content
```
- ~ Measles vaccination (see chapter 18)
- ~ Avoid contact between infected and uninfected persons
- ~ Educate the public against the common local myths e.g. stopping to feed meat and fish to measles patients
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.3.3 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.3 VIRAL INFECTIONS > 2.3.6 VIRAL HAEMORRHAGIC FEVERS > 2.3.6.1 Ebola and Marburg

### 49. narrative-0435
**Pages:** ? | **Section:** 2.3.6.1 Risk factors
**Validation:** No validation data

**Audit hash:** `69ffecf106b5f5c3...`

#### Extracted Content
```
- ~ Communities around game parks
- ~ Communities in endemic area
- ~ Cultural practices like burial rituals
- ~ Poor infection control practices
- ~ History of exposure to infected people in the last 2 to 21 days i.e sexual partner, breastfeeding mothers
- ~ Recent contact with infected animals e.g. monkeys, bats, infected game meat
- ~ Clinical features
- ~ Early signs (non specific): sudden fever, weakness, headache, muscle pains, loss of appetite, conjunctivitis
- ~ Late signs:
- ~ Diarrhoea (watery or bloody), vomiting
- ~ Mucosal and gastrointestinal bleeding: chest pain, respiratory distress, circulatory shock
- ~ CNS dysfunction, confusion, seizures
- ~ Miscarriage inpregnancy
- ~ Elevated AST and ALT, kidney injury, electrolyte abnormalities
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.3.6.1 Risk factors match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 50. narrative-0441
**Pages:** ? | **Section:** 2.3.6.1 Dead Body handling
**Validation:** No validation data

**Audit hash:** `781abcc5846c9959...`

#### Extracted Content
```
-  Avoid washing or touching the dead f There should be no gathering at funerals. The dead should be buried promptly by a designated burial team
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.3.6.1 Dead Body handling match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 51. narrative-0442
**Pages:** ? | **Section:** 2.3.6.1 Prevention
**Validation:** No validation data

**Audit hash:** `4bc01702ac7e9e67...`

#### Extracted Content
```
- ~ Health education of the population (e.g. avoid eating wildanimals)
- ~ Effective outbreak communication and having haemorrhagic viral fever protocols in place
- ~ Appropriate safety gear for patients/health workers insuspect cases
- ~ Modification of burial practices
- ~ Use of condoms
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.3.6.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.3 VIRAL INFECTIONS > 2.3.7 COVID-19 Disease

### 52. narrative-0460
**Pages:** ? | **Section:** 2.3.7 Prevention
**Validation:** No validation data

**Audit hash:** `a2c0055fa2494cb3...`

#### Extracted Content
```
- ~ Vaccination (Refer to chapter 18: Immunization)
- ~ Epidemic preparedness i.e. prompt detection and treatment
- ~ Infection Prevention and control measures including Mask wearing, social distancing, regular handwashing, avoid shaking hands etc.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 2.3.7 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.4 HELMINTHES PARASITES > 2.4.1 Intestinal Worms

### 53. narrative-0465
**Pages:** ? | **Section:** 2.4.1 Prevention
**Validation:** No validation data

**Audit hash:** `12b3d55e4a8c22c4...`

#### Extracted Content
```
- ~ Proper faecal disposal
- ~ Personal and food hygiene
- ~ Regular deworming of children every 3-6 months
- ~ Avoid walking barefoot
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.4.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.4 HELMINTHES PARASITES > 2.4.3 Dracunculiasis (Guinea Worm) ICD10 CODE: B72

### 54. narrative-0485
**Pages:** ? | **Section:** 2.4.3 Prevention
**Validation:** No validation data

**Audit hash:** `745f56dbda23bded...`

#### Extracted Content
```
-  Filter or boil drinking water
-  Infected persons should avoid all contact with sources ofdrinking water
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.4.3 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.4 HELMINTHES PARASITES > 2.4.6 Schistosomiasis (Bilharziasis) ICD10 CODE: B65.1

### 55. narrative-0505
**Pages:** ? | **Section:** 2.4.6 Prevention
**Validation:** No validation data

**Audit hash:** `beb8dbfdcb9ab168...`

#### Extracted Content
```
- ~ Avoid urinating or defecating in or near water
- ~ Avoid washing or stepping in contaminated water
- ~ Effective treatment of cases
- ~ Clear bushes around landing sites
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.4.6 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.5 PROTOZOAL PARASITES > 2.5.2 Malaria ICD10 CODE: B50 > 2.5.2.2 Complicated/Severe Malaria ICD10 CODE: B50.0, B50.8

### 56. narrative-0518
**Pages:** ? | **Section:** 2.5.2.2 Complicated/Severe Malaria ICD10 CODE: B50.0, B50.8
**Validation:** No validation data | **Condition:** Malaria

**Audit hash:** `999f181f95117cdc...`

#### Extracted Content
```
It is an immediate threat to life and is therefore a medical emergency. Malaria is regarded as severe if there are asexual forms of P. falciparum in blood plus one or more of the following complications in the table below.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 2.5.2.2 Complicated/Severe Malaria ICD10 CODE: B50.0, B50.8 match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.5 PROTOZOAL PARASITES > 2.5.2 Malaria ICD10 CODE: B50 > 2.5.3.3 Management of Complications of Severe Malaria

### 57. narrative-0536
**Pages:** ? | **Section:** 2.5.3.3 Management of RDT/Blood Smear Negative Ptients
**Validation:** No validation data | **Condition:** Malaria

**Audit hash:** `af9c56d12d153239...`

#### Extracted Content
```
Patients who have a negative malaria test (most likely, if RDT is used) do not have malaria so other causes of fever have to be investigated for appropriate treatment.

Uganda Clinical Guidelines 2023

CHAPTER 2: Infectious Diseases

177

Uganda Clinical Guidelines 2023

CHAPTER 2: Infectious Diseases

178

- ~ Re-assess patient history, clinical signs and laboratory results. Consider other frequent causes of fever such as:
-  If running nose, sore throat and cough: viral upper respiratory infection
-  If swollen tonsils with exudate on it: tonsilitis
-  If ear pain and discharge: otitis
-  If cough, rapid breathing and difficulty in breathing: pneumonia
-  If urinary symptoms: urinary tract infection
-  If vomiting, diarrhoea and abdominal pain: gastro-enteritis
-  If skin rash: measles or other viral rash
- ~ If malaria is still suspected, investigate according to the flowchart below
-  If signs/symptoms of severe malaria, RDT and blood slide negative but no other diagnosis is found, consider treating for malaria anyway but repeat RDTs after 24 hours to confirm.Also add a broad spectrum antibiotic
-  If RDT and blood slide negative, no signs of other illness and no signs of severe sickness (patient has no danger signs) treat symptomatically with antipyretics, advise patient to return immediately if condition worsens or in 2 days if fever persists.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 2.5.3.3 Management of RDT/Blood Smear Negative Ptients match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.5 PROTOZOAL PARASITES > 2.5.2 Malaria ICD10 CODE: B50 > 2.5.3.4 Malaria Prophylaxis

### 58. narrative-0538
**Pages:** ? | **Section:** 2.5.3.4 Malaria Prophylaxis
**Validation:** No validation data | **Condition:** Malaria

**Audit hash:** `8fcb5d0ced53db3a...`

#### Extracted Content
```
Not recommended for all those living in a highly endemic area like Uganda. However, it is recommended for certain high-risk groups but is not 100% effective

Uganda Clinical Guidelines 2023

CHAPTER 2: Infectious Diseases

179

Uganda Clinical Guidelines 2023

CHAPTER 2: Infectious Diseases

180
```

#### Extracted Clinical Flags
- **Contraindications:** all those living in a highly endemic area like Uganda

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: all those living in a highly endemic area like Uganda.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.5.3.4 Malaria Prophylaxis match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.5 PROTOZOAL PARASITES > 2.5.2 Malaria ICD10 CODE: B50 > 2.5.3.5 Malaria Prevention and Control

### 59. narrative-0540
**Pages:** ? | **Section:** 2.5.3.5 Reduce human-mosquito contact
**Validation:** No validation data | **Condition:** Malaria

**Audit hash:** `7822cb3d8385cf7c...`

#### Extracted Content
```
- ~ Use insecticide-treated materials (e.g. bed nets)
- ~ Destroy adult mosquitoes by indoor residual spraying of dwellings with insecticide or use of knock-down sprays
- ~ Screen houses
- ~ Carefully select house sites avoiding mosquito-infested areas
- ~ Wear clothes which cover the arms and legs and use repellent mosquito coils and creams/sprays on the skin when sitting outdoors at night
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.5.3.5 Reduce human-mosquito contact match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 2.5 PROTOZOAL PARASITES > 2.5.4 Human African Trypanosomiasis (Sleeping Sickness) ICD10 CODE: B56

### 60. narrative-0543
**Pages:** ? | **Section:** 2.5.4 Cause
**Validation:** No validation data

**Audit hash:** `4e660badc6dbdefd...`

#### Extracted Content
```
- ~ Trypanosoma rhodesiense (mostly in the Central and Eastern regions of Uganda)
- ~ Trypanosoma gambiense (mostly in West Nile region)
- ~ Clinical features
- ~ May be history of tsetse fly bite and swelling at site of bite after 7-14 days (more often in T. rhodesiense, rarely in T. Gambiense)

Uganda Clinical Guidelines 2023

CHAPTER 2: Infectious Diseases

181

Uganda Clinical Guidelines 2023

CHAPTER 2: Infectious Diseases

182
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.5.4 Cause match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 61. narrative-0551
**Pages:** ? | **Section:** 2.5.4 Adults &gt;15 years
**Validation:** No validation data

**Audit hash:** `eb8ec1777d26e117...`

#### Extracted Content
```
- -Nifurtimox/Elfornithine combination therapy (NECT)
- -Nifurtimox: 5 mg/kg every 8 hours orally for 10
- -days (15 mg/kg/day)
- -Plus Eflornithine 200 mg/kg 12 hourly for 7 days (400 mg/kg/day). Dilute Eflornithine dose of 200 mg/kg into 250 ml of distilled water and administer the infusion over at least 2 hours (50 drops/minute)
- -Infusions are given slowly to prevent convulsions
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.5.4 Adults &gt;15 years match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 62. narrative-0552
**Pages:** ? | **Section:** 2.5.4 Note
**Validation:** No validation data

**Audit hash:** `075631f354ec9bf3...`

#### Extracted Content
```
Corticosteroids: Should be given to patients with late trypanosomiasis on melarsoprol who may have

- ~ hypoadrenalism - the steroids may also reduce any drug reactions
- ~ Do not give hydrocortisone after day 24, even though the melarsoprol treatment is not yet complete
- ~ If prednisolone is used instead of hydrocortisone, the anti-inflammatory action is similar but the correction of the hypoadrenalism will be much less marked
- ~ Suramin: Do not use this medicine for early or late stage
- T . gambiense treatment in onchocerciasis-endemic areas as it may cause blindness in any onchocerciasis-infected patients by killing th e filar iae in the eye
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 2.5.4 Note match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.1 HIV INFECTION AND ACQUIRED IMMUNODEFICIENCY SYNDROME (AIDS) ICD 10 CODE: B20 > 3.1.1 Clinical Features of HIV

### 63. narrative-0560
**Pages:** ? | **Section:** 3.1.1 Clinical Features of HIV
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `c6e20375f82c9f3e...`

#### Extracted Content
```
The WHO Clinical Staging of HIV for adults and children in the tables below shows the typical clinical features of HIV infection. The staging is based on demonstration of one or more opportunistic infections or ke y findi ngs and correlates with disease progression and prognosis. Clinical staging should be performed at HIV diagnosis, on entry into HIV care, at ART initiation and at every visit hereafter to help guide patient care and monitor disease progress.

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

187

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

188
```

#### Extracted Clinical Flags
- **Special populations:** HIV diagnosis, on entry into HIV care, at ART initiation and at every visit hereafter to help guide 

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 3.1.1 Clinical Features of HIV match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.1 HIV INFECTION AND ACQUIRED IMMUNODEFICIENCY SYNDROME (AIDS) ICD 10 CODE: B20 > 3.1.2 Diagnosis and Investigations of HIV

### 64. narrative-0568
**Pages:** ? | **Section:** 3.1.2 HIV Testing Algorithm using the HIV-Syphilis Duo Kit in MCH Settings
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `9c6a61dfa9246342...`

#### Extracted Content
```
Serological testing is available from HC2 level.

In children below 18 months, testing is virological, that is based on direct detection of viral DNA (DNA-PCR).

Virological testing (DNA-PCR and viral load) is done on DBS (dried blood spots) samples which can be collected from HC2 and are sent to a central national laboratory through the hub system.

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

193

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

194
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 3.1.2 HIV Testing Algorithm using the HIV-Syphilis Duo Kit in MCH Settings match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.1 HIV INFECTION AND ACQUIRED IMMUNODEFICIENCY SYNDROME (AIDS) ICD 10 CODE: B20 > 3.1.6 Monitoring of ART

### 65. narrative-0593
**Pages:** ? | **Section:** 3.1.6 Monitoring of ART
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `257444cae52e93ac...`

#### Extracted Content
```
- More efficient use of resources by avoiding overcrowding and long waiting times
-  More focus on unstable/complex patients

(Refer to MOH HIV/ART guidelines for more details).
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 3.1.6 Monitoring of ART match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.1 HIV INFECTION AND ACQUIRED IMMUNODEFICIENCY SYNDROME (AIDS) ICD 10 CODE: B20 > 3.1.7 ARV Toxicity

### 66. narrative-0601
**Pages:** ? | **Section:** 3.1.7 ARV Toxicity
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `34e032f09bbd7f02...`

#### Extracted Content
```
ARV drugs can cause a wide range of toxicities, from mild to life threatening. Active monitoring and management of toxicities and side effects is important not only to avoid negative medical outcome but also to ensure that they do not negatively affect adherence.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 3.1.7 ARV Toxicity match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.1 HIV INFECTION AND ACQUIRED IMMUNODEFICIENCY SYNDROME (AIDS) ICD 10 CODE: B20 > 3.1.9 Mother-to-Child Transmission of HIV > 3.1.9.3 Care of HIV Exposed Infant

### 67. narrative-0629
**Pages:** ? | **Section:** 3.1.9.3 Immunisation
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `7d58e64af1cae612...`

#### Extracted Content
```
In case of missed BCG at birth, do not give if child has symptomatic HIV

-  Avoid yellow fever vaccine in symptomatic HIV
-  Measles vaccine can be given even in symptomatic HIV
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 3.1.9.3 Immunisation match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.1 HIV INFECTION AND ACQUIRED IMMUNODEFICIENCY SYNDROME (AIDS) ICD 10 CODE: B20 > 3.1.10 OPPORTUNISTIC INFECTIONS IN HIV > 3.1.10.1 Tuberculosis and HIV Co-Infection

### 68. narrative-0637
**Pages:** ? | **Section:** 3.1.10.1 Second line ART for patients with TB
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `712cd212af240c15...`

#### Extracted Content
```
- ~ There are significant drug interactions with PIs and rifampicin.
- ~ If rifabutin is available, it may be used in place of rifampicin with ATV/r or LPV/r, but it is contraindicated in patients with WBC counts below 1000/mm3.
- ~ Maintaining PI in second line regimens while switching from
```

#### Extracted Clinical Flags
- **Contraindications:** patients with WBC counts below 1000/mm3

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: patients with WBC counts below 1000/mm3.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 3.1.10.1 Second line ART for patients with TB match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 69. narrative-0638
**Pages:** ? | **Section:** 3.1.10.1 TB prevention
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `2edd3fd8c7553cac...`

#### Extracted Content
```
- ~ BCG immunisation: it protects children against severe forms of TB. It can be given at birth. If delayed, avoid in symptomatic HIV
- ~ IPT (Isoniazid Preventive Treatment) (see section 5.3.2.3)
```

#### Extracted Clinical Flags
- **Contraindications:** symptomatic HIV
- ~ IPT (Isoniazid Preventive Treatment) (see section 5

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: symptomatic HIV
- ~ IPT (Isoniazid Preventive Treatment) (see section 5.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 3.1.10.1 TB prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.1 HIV INFECTION AND ACQUIRED IMMUNODEFICIENCY SYNDROME (AIDS) ICD 10 CODE: B20 > 3.1.10 OPPORTUNISTIC INFECTIONS IN HIV > 3.1.10.3 Hepatitis B and HIV Co-Infection ICD10 CODE: B18

### 70. narrative-0645
**Pages:** ? | **Section:** 3.1.10.3 Prevention of HBV infection
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `c620e42e38c7f627...`

#### Extracted Content
```
- ~ Counseling: emphasize sexual transmission as well as the risks associated with sharing needles and syringes, tattooing or body-piercing
- ~ Advise patients with chronic HBV disease to avoid alcohol consumption
- ~ All household members and sexual partners of people living with HIV with HBV should be screened for HBsAG
- ~ HBV Vaccination is the most effective way to prevent HBV infection and its consequences
- -All HIV-infected patients who test negative on HBsAg
- -should be vaccinated with HBV vaccine
- -All sexual partners and contacts should receive HBV vaccination regardless of whether they are HIV-infected or not
```

#### Extracted Clinical Flags
- **Special populations:** HIV with HBV should be screened for HBsAG
- ~ HBV Vaccination is the most effective way to prevent H

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Special populations: HIV with HBV should be screened for HBsAG
- ~ HBV Vaccination is the most effective way to prevent H.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 3.1.10.3 Prevention of HBV infection match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.1 HIV INFECTION AND ACQUIRED IMMUNODEFICIENCY SYNDROME (AIDS) ICD 10 CODE: B20 > 3.1.10 OPPORTUNISTIC INFECTIONS IN HIV > 3.1.10.4 Pneumocystis Pneumonia

### 71. narrative-0646
**Pages:** ? | **Section:** 3.1.10.4 Pneumocystis Pneumonia
**Validation:** No validation data | **Condition:** Pneumonia

**Audit hash:** `681d573bd2db09a1...`

#### Extracted Content
```
ICD10 CODE: B59

Interstitial pneumonitis caused by the parasite Pneumocystis jirovecii (formerly carinii). It is common in severely immunosuppresed patients (e.g. in HIV).

- ~ Clinical features
- ~ Fever
- ~ Dry cough
- ~ Shortness of breath (significant hypoxemia)

~
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 3.1.10.4 Pneumocystis Pneumonia match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.1 HIV INFECTION AND ACQUIRED IMMUNODEFICIENCY SYNDROME (AIDS) ICD 10 CODE: B20 > 3.1.11 Prevention of HIV

### 72. narrative-0651
**Pages:** ? | **Section:** 3.1.11 Behavioural change
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `bd0351b34c2ce54c...`

#### Extracted Content
```
- ~ Always follow safe sex practices (e.g. use condoms; avoid multiple sexual partners)
- ~ Never share used needles, syringes, razors, hair shavers, nail cutters, and other sharp objects
- ~ Avoid tattooing, body-piercing, and scarification unless carried out under strictly hygienic conditions in properly controlled premises
- ~ Delay start of sexual activity in adolescence
- ~ Discourage cross generational and transactional sex
- ~ Avoid violence and abuse
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 3.1.11 Behavioural change match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 73. narrative-0655
**Pages:** ? | **Section:** 3.1.11 Post-rape care (see also section 1.2.6)
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `b2c92407bba0c305...`

#### Extracted Content
```
Health facilities should provide the following clinical services as part of post-rape care:

- ~ Initial assessment of the client
- ~ Rapid HIV testing and referral to care and treatmentif HIV-infected
- ~ Post-exposure prophylaxis (PEP) for HIV
- ~ STI screening/testing and treatment
- ~ Forensic interviews and examinations
- ~ Emergency contraception - if person reached within the first 72 hours
- ~ Counselling

The health facility should also identify, refer and link clients to non-clinical services

-  Some of the services include the following:
-  Long-term psycho-social support
-  Legal counseling
-  Police investigations, restraining orders
-  Child protection services (e.g. emergency out of family care, reintegration into family care or permanent options when reintegration into family is impossible)
-  Economic empowerment
-  Emergency shelters
-  Long-term case management

Reporting: Health facilities should use HMIS 105 to report Gender Based Violence (GBV)
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 3.1.11 Post-rape care (see also section 1.2.6) match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.2 SEXUALLY TRANSMITTED INFECTIONS (STI) > 3.2.2 Abnormal Vaginal Discharge Syndrome

### 74. narrative-0674
**Pages:** ? | **Section:** 3.2.2 Causes
**Validation:** No validation data

**Audit hash:** `ddbcb16c0356f3fe...`

#### Extracted Content
```
- ~ Can be a variety and often mixture of organisms
- ~ Vaginitis: by Candida albicanis, Trichomonas vaginalis or bacterial vaginosis (by Gardnerella vaginalis, Mycoplasma hominis)
- ~ Cervicitis: commonly due to gonorrhoea and chlamydia: usually asymptomatic and rarely a cause of abnormal vaginal discharge.
- ~ Clinical features
- ~ Increased quantity of discharge, abnormal colour and odour
- ~ Lower abdominal pain, itching and pain at sexual intercourse may be present
- ~ In Candida albicans vaginitis: very itchy thick or lumpy white discharge, red inflamed vulva
- ~ Trichomonas vaginalis: itchy greenish-yellow frothy discharge with offensive smell
- ~ Bacterial vaginosis: thin discharge with a fishy smell from the vagina

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

279

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

280

Candida vaginitis and bacterial vaginosis are NOT sexually transmitted diseases, even though sexual activity is a risk factor.

- ~ Gonorrhoea causes cervicitis and rarely vaginitis. Thereis a purulent thin mucoid slightly yellow pus discharge with no smell and non-itchy
- ~ Chlamydia causes cervicitis which may present with a nonitchy, thin, colourless discharge
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 3.2.2 Causes match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.2 SEXUALLY TRANSMITTED INFECTIONS (STI) > 3.2.8 Other Genital Infections > 3.2.8.2 Painful Scrotal Swelling

### 75. narrative-0706
**Pages:** ? | **Section:** 3.2.8.2 Causes
**Validation:** No validation data

**Audit hash:** `160084c52b1a293f...`

#### Extracted Content
```
-  Usually caused by N. gonorrhoea, Chlamydia
-  Clinical features
-  Acute painful and tender unilateral swelling of epididymus and testis, with or without urethral discharge
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 3.2.8.2 Causes match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.2 SEXUALLY TRANSMITTED INFECTIONS (STI) > 4.1.2 Infective Endocarditis ICD10 CODE: I33.0

### 76. narrative-0735
**Pages:** ? | **Section:** 4.1.2 Prevention
**Validation:** No validation data

**Audit hash:** `759f962c4f107f3e...`

#### Extracted Content
```
-  Prophylaxis in case of dental procedures and tonsillectomy in patients at risk (valvular defects, congenital heart disease, prosthetic valve). Give amoxicillin 2 g (50 mg/kg for children) as a single dose, 1 hour before the procedure.
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 4.1.2 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.2 SEXUALLY TRANSMITTED INFECTIONS (STI) > 4.1.4 Pulmonary Oedema ICD10 CODE: I50.21

### 77. narrative-0750
**Pages:** ? | **Section:** 4.1.4 Caution
**Validation:** No validation data

**Audit hash:** `45412e52b444e2e9...`

#### Extracted Content
```
- Do not give loading dose if patient has had digoxin within the past 14 days but give maintenance dose
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 4.1.4 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 78. narrative-0751
**Pages:** ? | **Section:** 4.1.4 Prevention
**Validation:** No validation data

**Audit hash:** `ca89b6fea3b289b8...`

#### Extracted Content
```
-  Early diagnosis and treatment of cardiac conditions
-  Compliance with treatment for chronic cardiac conditions
-  Avoid fluid overload
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 4.1.4 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.2 SEXUALLY TRANSMITTED INFECTIONS (STI) > 4.1.6 Hypertension ICD10 code: I10

### 79. narrative-0768
**Pages:** ? | **Section:** 4.1.6 Step7
**Validation:** No validation data | **Condition:** Hypertension

**Audit hash:** `fb850943b9c504b4...`

#### Extracted Content
```
If BP is ≥ 140/90mmHg, refer for further management to a higher level of care.

- Provision for specific patients
- Assess the cardiovascular disease (CVD) risk in all patients with hypertension.
- Patients with diabetes, coronary heart disease, stroke or chronic kidney disease are considered having a high CVD risk.
- The target BP is &lt;130/80 mmHg in people with high CVD risk.
- Start statin (atorvastatin 20-40 mg once daily or simvastatin 20-40 mg once daily) and aspirin 75mg in people with prior heart attack or ischemic stroke. Consider statin in people at high risk.
- Start beta blocker (Atenolol 50mg or Bisoprolol 5mg or Nebivolol 5mg once daily) in people with heart attack in past 3 years.
- A combination of ACEI or ARB and a CCB or a diuretic is recommended as initial therapy in patients with chronic kidney disease.
- For hypertension secondary to thyroid disease consider adding Propranolol 40mg twice daily
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 4.1.6 Step7 match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.2 SEXUALLY TRANSMITTED INFECTIONS (STI) > 4.1.9 Rheumatic Fever

### 80. narrative-0798
**Pages:** ? | **Section:** 4.1.9 Prevention
**Validation:** No validation data

**Audit hash:** `7757d1708c30ebe1...`

#### Extracted Content
```
- ~ Early diagnosis and treatment of group A Streptococcus throat infection
- ~ Avoid overcrowding, good housing
- ~ Good nutrition
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 4.1.9 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 3.2 SEXUALLY TRANSMITTED INFECTIONS (STI) > 4.1.10 Rheumatic Heart Disease ICD10 CODE: I05-I09

### 81. narrative-0807
**Pages:** ? | **Section:** 4.1.10 Investigations
**Validation:** No validation data | **Condition:** Cardiac disease

**Audit hash:** `22bc10070377c6b8...`

#### Extracted Content
```
-  CT scan of the brain

In the absence of neuroimaging, the following clinical features may help to distinguish the stroke subtypes:
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 4.1.10 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.1 NON-INFECTIOUS RESPIRATORY DISEASES > 5.1.1 Asthma

### 82. narrative-0814
**Pages:** ? | **Section:** 5.1.1 Investigations
**Validation:** No validation data | **Condition:** Asthma

**Audit hash:** `6c3de0ff304efab1...`

#### Extracted Content
```
-  Diagnosis is mainly by clinical features
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.1.1 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.1 NON-INFECTIOUS RESPIRATORY DISEASES > 5.1.1 Asthma > 5.1.1.2 Chronic Asthma

### 83. narrative-0823
**Pages:** ? | **Section:** 5.1.1.2 General principles of management
**Validation:** No validation data | **Condition:** Asthma

**Audit hash:** `78b32433774937b9...`

#### Extracted Content
```
- ~ Follow a stepped approach
-  Before initiating a new drug, check that diagnosis is correct, compliance and inhaler technique are correct and eliminate trigger factors for acute exacerbations
- ~ Start at the step most appropriate to initial severity
- ~ Rescue course
-  Give a 3-5 days "rescue course" of prednisolone at any step and at any time as required to control acute exacerbations of asthma at a dose of:

Child &lt; 1 year: 1-2 mg/kg daily; 1-5 years: up to 20 mg daily; 5-15 years: Up to 40 mg daily; adult: 40-60 mg daily for up to 3-5 days.

- ~ Stepping down
-  Review treatment every 3-6 months
-  If control is achieved, stepwise reduction may be possible
-  If treatment started recently at Step 4 (or contained corticosteroid tablets, see below), reduction may take place after a short interval; in other patients 1-3 months or longer of stability may be needed before stepwise reduction can be done
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.1.1.2 General principles of management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 84. narrative-0826
**Pages:** ? | **Section:** 5.1.1.2 Caution
**Validation:** No validation data | **Condition:** Asthma

**Audit hash:** `8ce91f1802c8e8c2...`

#### Extracted Content
```
-  Do not give medicines such as morphine, propranolol, or other B-blockers to patients with asthma as they worsen respiratory problems
-  Do not give sedatives to children with asthma, even if they are restless

Uganda Clinical Guidelines 2023

CHAPTER 5: Respiratory Diseases

339

Uganda Clinical Guidelines 2023

CHAPTER 5: Respiratory Diseases

340
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.1.1.2 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 85. narrative-0827
**Pages:** ? | **Section:** 5.1.1.2 Prevention
**Validation:** No validation data | **Condition:** Asthma

**Audit hash:** `b5b97e938ed04492...`

#### Extracted Content
```
- ~ Avoid precipitating factors e.g.
-  Cigarette smoking
-  Acetylsalicylic acid
-  Known allergens such as dust, pollens, animal skins
-  Exposure to cold air
- ~ Exercise can precipitate asthma in children, advise them to keep an inhaler handy during sports and play
- ~ Effectively treat respiratory infections
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.1.1.2 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.2 INFECTIOUS RESPIRATORY DISEASES > 5.2.1 Bronchiolitis

### 86. narrative-0843
**Pages:** ? | **Section:** 5.2.1 Note
**Validation:** No validation data | **Condition:** Respiratory disease

**Audit hash:** `1696e56798431915...`

#### Extracted Content
```
-  Antibiotics are usually not needed for bronchiolitis since it is viral.
-  Steroids are not recommended
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.2.1 Note match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 87. narrative-0844
**Pages:** ? | **Section:** 5.2.1 Prevention
**Validation:** No validation data | **Condition:** Respiratory disease

**Audit hash:** `eef3147e0c1512f3...`

#### Extracted Content
```
-  Avoid exposure to cold and viral infections
-  Proper handwashing after contact with patients
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.2.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.2 INFECTIOUS RESPIRATORY DISEASES > 5.2.2 Acute Bronchitis ICD10 CODE: J20

### 88. narrative-0849
**Pages:** ? | **Section:** 5.2.2 Differential diagnosis
**Validation:** No validation data | **Condition:** Respiratory disease

**Audit hash:** `9a0abaa7b7205654...`

#### Extracted Content
```
- ~ Bronchial asthma, emphysema
- ~ Pneumonia, tuberculosis

Investigations

-  Diagnosis based on clinical features
-  Chest X-ray
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.2.2 Differential diagnosis match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 89. narrative-0850
**Pages:** ? | **Section:** 5.2.2 Prevention
**Validation:** No validation data | **Condition:** Respiratory disease

**Audit hash:** `b1a69fb549124c04...`

#### Extracted Content
```
- ~ Avoid predisposing factors above.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.2.2 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.2 INFECTIOUS RESPIRATORY DISEASES > 5.2.3 Coryza (Common Cold)

### 90. narrative-0857
**Pages:** ? | **Section:** 5.2.3 Prevention
**Validation:** No validation data | **Condition:** Respiratory disease

**Audit hash:** `53a97f790bceba2b...`

#### Extracted Content
```
- ~ Avoid contact with infected persons
- ~ Include adequate fresh fruits and vegetables in the diet
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.2.3 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.2 INFECTIOUS RESPIRATORY DISEASES > 5.2.4 Acute Epiglottitis ICD10 CODE: J05.1

### 91. narrative-0862
**Pages:** ? | **Section:** 5.2.4 Caution
**Validation:** No validation data | **Condition:** Respiratory disease

**Audit hash:** `207ce4d4db696f69...`

#### Extracted Content
```
-  Avoid tongue depression examination as this may cause complete airway blockage and sudden death
-  Do not force child to lie down as it may precipitate airway obstruction

Uganda Clinical Guidelines 2023

CHAPTER 5: Respiratory Diseases

349

Uganda Clinical Guidelines 2023

CHAPTER 5: Respiratory Diseases

350
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.2.4 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.2 INFECTIOUS RESPIRATORY DISEASES > 5.2.5 Influenza (" Flu") ICD10 CODE: J9-11

### 92. narrative-0870
**Pages:** ? | **Section:** 5.2.5 Prevention
**Validation:** No validation data | **Condition:** Respiratory disease

**Audit hash:** `9089ca2a36141a80...`

#### Extracted Content
```
- ~ Avoid contact with infected persons
- ~ Inactivated Influenza vaccine yearly (for vulnerable populations)

Uganda Clinical Guidelines 2023

CHAPTER 5: Respiratory Diseases

351

Uganda Clinical Guidelines 2023

CHAPTER 5: Respiratory Diseases

352
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.2.5 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.2 INFECTIOUS RESPIRATORY DISEASES > 5.2.7 Acute Laryngotracheobronchitis (Croup)

### 93. narrative-0880
**Pages:** ? | **Section:** 5.2.7 Caution
**Validation:** No validation data | **Condition:** Respiratory disease

**Audit hash:** `6d08476a2c372b63...`

#### Extracted Content
```
 Avoid throat examination. Gagging can cause acute obstruction
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.2.7 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 94. narrative-0881
**Pages:** ? | **Section:** 5.2.7 Prevention
**Validation:** No validation data | **Condition:** Respiratory disease

**Audit hash:** `09074a62d7919449...`

#### Extracted Content
```
- ~ Avoid contact with infected persons
- ~ Isolate infected persons
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.2.7 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.2 INFECTIOUS RESPIRATORY DISEASES > 5.2.8 Pertussis (Whooping Cough)

### 95. narrative-0889
**Pages:** ? | **Section:** 5.2.8 Prevention
**Validation:** No validation data | **Condition:** Respiratory disease

**Audit hash:** `1da55513a2138ba0...`

#### Extracted Content
```
- ~ Educate parents on the importance of following the routine childhood immunisation schedule:
- ~ Ensure good nutrition
- ~ Avoid overcrowding
- ~ Booster doses of vaccine in exposed infants
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.2.8 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.3 TUBERCULOSIS (TB)

### 96. narrative-0929
**Pages:** ? | **Section:** 5.3 Other investigations
**Validation:** No validation data | **Condition:** Tuberculosis

**Audit hash:** `8a638da093e7e5e8...`

#### Extracted Content
```
-  X- ray, abdominal ultrasound, biopsies etc. can be used for sputum and GeneXpert negative patients or in case of extrapulmonary TB according to clinical judgement
-  TST can be used as a supportive test to guide decision to treat for TB in children
-  putum culture and Drug susceptibility test: is a confirmatory test for TB and also provides resistance pattern to TB medicines. Do this test for:
-  Patients with Rifampicin resistance reported with GeneXpert
-  Also patients on first-line treatment who remain positive at 2 months and are reported Rifampicin sensitive on GeneXpert
-  Patients suspected to be failing on first-line treatment

Note: All presumed and diagnosed TB patients should be offered an HIV test
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.3 Other investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.3 TUBERCULOSIS (TB) > 5.3.2 Management of TB

### 97. narrative-0945
**Pages:** ? | **Section:** 5.3.2 During the 6th month:
**Validation:** No validation data | **Condition:** Tuberculosis

**Audit hash:** `9d662c0f82a94524...`

#### Extracted Content
```
- -Sputum smear-negative, complete treatment and declare cured or treatment completed
- -Sputum smear-positive, diagnose treatment failure
- -Take sputum for GeneXpert to rule out rifampicin resistance and Xpert MTB/XDR where accessible, to rule out resistance to other drugs
- -If Rifampicin-resistant, refer for MDR-TB treatment
- -If Rifampicin-sensitive, restart first-line treatment, explore adherence issues
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 5.3.2 During the 6th month: match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 98. narrative-0947
**Pages:** ? | **Section:** 5.3.2 Note
**Validation:** No validation data | **Condition:** Tuberculosis

**Audit hash:** `7aa383c2a0281e2e...`

#### Extracted Content
```
-  Radiological monitoring- this method should not be used as the sole monitoring tool.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.3.2 Note match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 5.3 TUBERCULOSIS (TB) > 5.3.2 Management of TB > 5.3.2.2 Prevention and Infection Control of TB

### 99. narrative-0958
**Pages:** ? | **Section:** 5.3.2.2 General hygiene
**Validation:** No validation data | **Condition:** Tuberculosis

**Audit hash:** `38e361daff306db6...`

#### Extracted Content
```
- ~ Avoidance of overcrowding
- ~ Avoid drinking unboiled milk

Uganda Clinical Guidelines 2023

CHAPTER 5: Respiratory Diseases

385

Uganda Clinical Guidelines 2023

CHAPTER 5: Respiratory Diseases

386

- ~ Cough hygiene (cover cough with pieces of cloth, washing hands with soap, proper disposal of sputum)
- ~ Good nutrition
- ~ Promote good ventilation in housing &amp; transport
- · Open ventilators, windows &amp; doors that allow air exchange
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 5.3.2.2 General hygiene match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 6.1 GASTROINTESTINAL EMERGENCIES > 6.1.3 Upper Gastrointestinal Bleeding ICD10 CODE: K92.2

### 100. narrative-0980
**Pages:** ? | **Section:** 6.1.3 Upper Gastrointestinal Bleeding ICD10 CODE: K92.2
**Validation:** No validation data

**Audit hash:** `cb86e8bc8a7aa1ab...`

#### Extracted Content
```
Bleeding from the upper gastrointestinal tract (oesophagus, stomach and duodenum). It can be a medical emergency.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 6.1.3 Upper Gastrointestinal Bleeding ICD10 CODE: K92.2 match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 6.2 GASTROINTESTINAL INFECTIONS > 6.2.1 Amoebiasis

### 101. narrative-0996
**Pages:** ? | **Section:** 6.2.1 Causes
**Validation:** No validation data

**Audit hash:** `ecd218aa7a983ed2...`

#### Extracted Content
```
- ~ Protozoan Entamoeba histolytica

Clinical features

It may present as:

Uganda Clinical Guidelines 2023

CHAPTER 6: Gastrointestinal and Hepatic Diseases

405

Uganda Clinical Guidelines 2023

CHAPTER 6: Gastrointestinal and Hepatic Diseases

406
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 6.2.1 Causes match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 102. narrative-1002
**Pages:** ? | **Section:** 6.2.1 Caution
**Validation:** No validation data

**Audit hash:** `303ccdf1109bd01c...`

#### Extracted Content
```
-  Metronidazole/tinidazole: do not use in 1st trimester of pregnancy; avoid alcohol during treatment and for 48 hours thereafter
-  Metronidazole: Take after food
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 6.2.1 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 6.2 GASTROINTESTINAL INFECTIONS > 6.2.2 Bacillary Dysentery (Shigellosis) ICD10 CODE: A03.9

### 103. narrative-1010
**Pages:** ? | **Section:** 6.2.2 Caution
**Validation:** No validation data

**Audit hash:** `6460984fbd97df7e...`

#### Extracted Content
```
-  Ciprofloxacin, doxycycline: usually contraindicated in pregnancy and children &lt; 8 years but single dose in cholera should not provoke adverse effect
-  Alternative: erythromycin 500 mg every 6 hours for 5 days
```

#### Extracted Clinical Flags
- **Contraindications:** pregnancy and children &lt

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: pregnancy and children &lt.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 6.2.2 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 6.3 GASTROINTESTINAL DISORDERS > 6.3.3 Gastroesophageal Reflux Disease (GERD/GORD) ICD10 CODE: K21

### 104. narrative-1034
**Pages:** ? | **Section:** 6.3.3 Management
**Validation:** No validation data

**Audit hash:** `08cda0e29630065e...`

#### Extracted Content
```
Lifestyle modifications include the following:

-  Losing weight (if overweight)
-  Avoiding alcohol, chocolate, citrus juice, and tomato-based products also suggest avoiding peppermint, coffee, and possibly the onion family, spicy foods, food with high fat content, carbonated beverages)
-  Avoiding large meals
-  Waiting 3 hours after a meal before lying down or eating within 2-3 hours before bedtime should be avoided
-  Elevating the head of the bed by 8 inches
-  Avoid tight fitting clothes
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 6.3.3 Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 6.3 GASTROINTESTINAL DISORDERS > 6.3.4 Gastritis ICD10 CODE: K29

### 105. narrative-1041
**Pages:** ? | **Section:** 6.3.4 Caution
**Validation:** No validation data

**Audit hash:** `9ab79e255805dce4...`

#### Extracted Content
```
-  Acetylsalicylic acid and other NSAIDS are contraindicated in patients with gastritis
```

#### Extracted Clinical Flags
- **Contraindications:** patients with gastritis

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: patients with gastritis.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 6.3.4 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 106. narrative-1042
**Pages:** ? | **Section:** 6.3.4 Prevention
**Validation:** No validation data

**Audit hash:** `cb10380bd79448a4...`

#### Extracted Content
```
- ~ Avoid spices, tobacco, alcohol, and carbonated drinks
- ~ Encourage regular, small, and frequent meals
- ~ Encourage milk intake
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 6.3.4 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 6.5 HEPATIC AND BILIARY DISEASES > 6.5.1 Viral Hepatitis > 6.5.1.1 Acute Hepatitis ICD10 CODES: B15, B16, B17, B19

### 107. narrative-1076
**Pages:** ? | **Section:** 6.5.1.1 Caution
**Validation:** No validation data | **Condition:** Hepatitis

**Audit hash:** `e27d88ad3e1b6ef4...`

#### Extracted Content
```
-  Avoid drugs generally but especially sedatives and hepatotoxic drugs
-  Ensure effective infection control measures e.g. institute barrier nursing, personal hygiene
-  Patient isolation is not necessary unless there is high suspicion of viral haemorrhagic fevers
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 6.5.1.1 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 108. narrative-1077
**Pages:** ? | **Section:** 6.5.1.1 Caution
**Validation:** No validation data | **Condition:** Hepatitis

**Audit hash:** `e27d88ad3e1b6ef4...`

#### Extracted Content
```
-  Avoid drugs generally but especially sedatives and hepatotoxic drugs
-  Ensure effective infection control measures e.g. institute barrier nursing, personal hygiene
-  Patient isolation is not necessary unless there is high suspicion of viral haemorrhagic fevers
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 6.5.1.1 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 6.5 HEPATIC AND BILIARY DISEASES > 6.5.2 Chronic Hepatitis B Infection

### 109. narrative-1084
**Pages:** ? | **Section:** 6.5.2 Health education
**Validation:** No validation data | **Condition:** Hepatitis

**Audit hash:** `882cd5c5fd49f7df...`

#### Extracted Content
```
- ~ Mangement is lifelong because of the need to monitor hepatitis
- ~ Bed rest
- ~ Urge patient to avoid alcohol as it worsens disease
- ~ Immunisation of household contacts
- ~ Do not share items that the patient puts in mouth (e.g. toothbrushes, cutlery) and razor blades
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 6.5.2 Health education match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 7.1 RENAL DISEASES > 7.1.2 Chronic Kidney Disease (CKD) ICD10 CODE: N18

### 110. narrative-1153
**Pages:** ? | **Section:** 7.1.2 Prevention
**Validation:** No validation data | **Condition:** Renal disease

**Audit hash:** `0d778d181ece8c00...`

#### Extracted Content
```
- ~ Screening of high risk patients
- ~ Optimal treatment of risk factors
- ~ Treatments to slow progression in initial phases
- ~ Avoidance of nephrotoxic drugs
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 7.1.2 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 7.1 RENAL DISEASES > 7.1.3 Use of Drugs in Renal Failure

### 111. narrative-1156
**Pages:** ? | **Section:** 7.1.3 Drugs to use with care in reduced doses
**Validation:** No validation data | **Condition:** Renal disease

**Audit hash:** `91ad72893ddd3bd6...`

#### Extracted Content
```
ACE inhibitors (e.g. captopril)

-  Amoxicillin
-  Chloramphenicol (avoid in severe impairment)
-  Ciprofloxacin r Cotrimoxazole r Diazepam
-  Digoxin
-  Insulin
-  Isoniazid-containing medicines
-  Pethidine (increase dose interval, avoid in severe impairment)
-  Phenobarbital
-  Propranolol
```

#### Extracted Clinical Flags
- **Contraindications:** severe impairment)
-  Ciprofloxacin r Cotrimoxazole r Diazepam
-  Digoxin
-  Insulin
-  Isoniazid-containing medicines
-  Pethidine (increase dose interval, avoid in severe impairment)
-  Phenobarbital
-  Propranolol

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: severe impairment)
-  Ciprofloxacin r Cotrimoxazole r Diazepam
-  Digoxin
-  Insulin
-  Isoniazid-containing medicines
-  Pethidine (increase dose interval, avoid in severe impairment)
-  Phenobarbital
-  Propranolol.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 7.1.3 Drugs to use with care in reduced doses match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 7.1 RENAL DISEASES > 7.1.4 Glomerulonephritis

### 112. narrative-1164
**Pages:** ? | **Section:** 7.1.4 Prevention
**Validation:** No validation data | **Condition:** Renal disease

**Audit hash:** `0f9fc993400df692...`

#### Extracted Content
```
- ~ Treat throat and skin infections promptly and effectively
- ~ Avoid overcrowding
- ~ Adequate ventilation in dwellings
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 7.1.4 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 7.2 UROLOGICAL DISEASES > 7.2.3 Prostatitis ICD10 CODE: N41

### 113. narrative-1186
**Pages:** ? | **Section:** 7.2.3 Clinical features
**Validation:** No validation data

**Audit hash:** `d6d8f4570effc8ee...`

#### Extracted Content
```
- ~ Fever, chills
- ~ Rectal, perineal and low back pain
- ~ Urinary urgency, frequency and dysuria
- ~ May cause acute urinary retention
- ~ At rectal examination: tender enlarged prostate (avoid vigorous examination)
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 7.2.3 Clinical features match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 7.2 UROLOGICAL DISEASES > 8.1.1 Addison's Disease

### 114. narrative-1214
**Pages:** ? | **Section:** 8.1.1 Prevention
**Validation:** No validation data

**Audit hash:** `9ca0259f360fc815...`

#### Extracted Content
```
- ~ Avoid self medication with steroids (prednisolone, dexamethasone)
- ~ Decrease steroids gradually if used for treatment durations longer than 2 weeks (see above)

Uganda Clinical Guidelines 2023

CHAPTER 8: Endocrine and Metabolic Diseases

469

Uganda Clinical Guidelines 2023

CHAPTER 8: Endocrine and Metabolic Diseases

470
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 8.1.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 7.2 UROLOGICAL DISEASES > 8.1.3 Diabetes Mellitus ICD10 CODE: E08-E13

### 115. narrative-1233
**Pages:** ? | **Section:** 8.1.3 Management of Type 1 Diabetes
**Validation:** No validation data | **Condition:** Diabetes

**Audit hash:** `a36813a5dc7a377f...`

#### Extracted Content
```
Insulin SC: 0.6 -1.5 IU/kg/day HC4 Children &lt;5 years: start with 0.5 IU/Kg/day, and refer to a paediatrician
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify Level of Care assignments (HC4) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 8.1.3 Management of Type 1 Diabetes match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 116. narrative-1240
**Pages:** ? | **Section:** 8.1.3 Caution
**Validation:** No validation data | **Condition:** Diabetes

**Audit hash:** `0805d714b62cc60f...`

#### Extracted Content
```
-  Metformin is contraindicated in advanced kidney disease
-  Do not use oral anti-diabetics in acute complications, and in acutely sick patients: use insulin for initial management
```

#### Extracted Clinical Flags
- **Contraindications:** advanced kidney disease
-  Do not use oral anti-diabetics in acute complications, and in acutely sick patients: use insulin for initial management

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: advanced kidney disease
-  Do not use oral anti-diabetics in acute complications, and in acutely sick patients: use insulin for initial management.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 8.1.3 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 9.1 NEUROLOGICAL DISORDERS

### 117. narrative-1279
**Pages:** ? | **Section:** 9.1 General principles
**Validation:** No validation data

**Audit hash:** `df8c8cf55b974239...`

#### Extracted Content
```
- ~ All suspected cases of non-convulsive epilepsy should be confirmed and treated by a specialist
- ~ Convulsive epilepsy can be diagnosed at hospital/HC3
- ~ level but drug refills should be available at lower levels
- ~ One brief isolated seizure does not need further treatment but review at 3 months and re-assessment. Treat patients with repeated episodes as per definition
- ~ Treatment can effectively control epilepsy in most cases
- ~ Treatment should include psychological and social support
- ~ Start with a single anti-epileptic medicine
- ~ Start with low doses and increase gradually according to response
- ~ If a patient has been seizure free for 2 years, consider gradual stopping of medication
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 9.1 General principles match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 118. narrative-1280
**Pages:** ? | **Section:** 9.1 Commonly used antiepileptics include:
**Validation:** No validation data

**Audit hash:** `60194d58907d194c...`

#### Extracted Content
```
- ~ Generalized tonic-clonic seizures
- ·Children &lt;2 years: phenobarbital or carbamazepine
- ·Children &gt;2 years: carbamazepine or valproate
- ~ Absence seizures: Valproate or ethosuximide
- ~ Caution: Avoid phenobarbital and phenytoin in children with intellectual disability and/or behavioural problems
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 9.1 Commonly used antiepileptics include: match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 119. narrative-1283
**Pages:** ? | **Section:** 9.1 Note
**Validation:** No validation data

**Audit hash:** `1f16c8e3961b039f...`

#### Extracted Content
```
-  In children, look for presence of associated intellectual disability or behavioural problems. If present, consider carbamazepine or valproate. (avoid phenobarbital and phenytoin) and manage associated intellectual disability or behavioural problem
-  All pregnant women with epilepsy should be referred to specialist for appropriate management (most
```

#### Extracted Clinical Flags
- **Special populations:** pregnant women with epilepsy should be referred to specialist for appropriate management (most

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Special populations: pregnant women with epilepsy should be referred to specialist for appropriate management (most.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 9.1 Note match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 120. narrative-1285
**Pages:** ? | **Section:** 9.1 Prevention
**Validation:** No validation data

**Audit hash:** `c57b05648cd1dc53...`

#### Extracted Content
```
- ~ Good antenatal care and delivery
- ~ Avoid causative factors

Uganda Clinical Guidelines 2023

CHAPTER 9: Mental, Neurological and Substance Use Disorders

495

Uganda Clinical Guidelines 2023

CHAPTER 9: Mental, Neurological and Substance Use Disorders

496
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 9.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 9.1 NEUROLOGICAL DISORDERS > 9.1.3 Headache ICD10 CODE: R51 > 9.1.3.1 Migraine ICD10 CODE: G43

### 121. narrative-1294
**Pages:** ? | **Section:** 9.1.3.1 Causes
**Validation:** No validation data

**Audit hash:** `6a20b30874a8eb30...`

#### Extracted Content
```
The cause is unknown but thought to be linked to:

- ~ Familial factors
- ~ Craniovascular disorders, which can be precipitated by: stress, anxiety, menstruation, flashing lights, hunger, lack of sleep, oestrogens (in COC), perfumes, tyramine- containing foods e.g. red wine, cheese, chocolate
- ~ Clinical features
- ~ Warning signs (aura): visual or sensory sympotms (flashing lights) preceeding the start of the headache
- ~ Migraine with warning signs is called migraine with aura. They are not always present
- ~ Moderate to severe episodic unilateral headache throbbing (pulsating)
- ~ Nausea and vomiting, sensitivity to light and sound
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 9.1.3.1 Causes match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 122. narrative-1297
**Pages:** ? | **Section:** 9.1.3.1 Prevention
**Validation:** No validation data

**Audit hash:** `379e8633190ad183...`

#### Extracted Content
```
- ~ Avoid precipitating factors
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 9.1.3.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 9.1 NEUROLOGICAL DISORDERS > 9.1.4 Dementia ICD10 CODE: F01, F03

### 123. narrative-1304
**Pages:** ? | **Section:** 9.1.4 Caution
**Validation:** No validation data

**Audit hash:** `99b72c8df9549687...`

#### Extracted Content
```
- ~ Avoid Diazepam: it can lead to falls and is often not effective
- ~ Prevention
- ~ Avoid and treat preventable causes
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 9.1.4 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 9.2 PSYCHIATRIC AND SUBSTANCE USE DISORDERS

### 124. narrative-1321
**Pages:** ? | **Section:** 9.2 Types and clinical features
**Validation:** No validation data

**Audit hash:** `fcd627319c870fd1...`

#### Extracted Content
```
- ~ Generalized anxiety: Unrealistic and excessive worry about almost everything
- ~ Panic attacks: Episodes of sudden onset of intense apprehension or fear; anxiety symptoms usually peak within 1015 minutes and resolve in a few minutes to one hour
- ~ Phobia: An excessive fear of a known stimulus (object or
- ~ situation) e.g. animals, water, confined space) causing the person to consciously avoid the object or situation

Each of the above clinical types will have one or more of the following manifestations:

- ~ Sleep, mood and concentration problems
- ~ Palpitations, dizziness, shortness of breath
- ~ Shakiness or tremors, excessive sweatiness
- ~ Easily frightened
- ~ Other symptoms: urinary frequency, hesitancy, or urgency, diarrhoea
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 9.2 Types and clinical features match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 125. narrative-1324
**Pages:** ? | **Section:** 9.2 Caution
**Validation:** No validation data

**Audit hash:** `daff94e29e92178a...`

#### Extracted Content
```
- Diazepam is addictive and abrupt cessation can cause withdrawal symptoms. Use for short periods and gradually reduce the dose. Avoid alcohol
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 9.2 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 9.2 PSYCHIATRIC AND SUBSTANCE USE DISORDERS > 9.2.2 Depression ICD10 CODE: F32, F33 > 9.2.2.2 Suicidal Behaviour/Self Harm ICD10 CODES: T14.91, Z91.5

### 126. narrative-1335
**Pages:** ? | **Section:** 9.2.2.2 Suicidal Behaviour/Self Harm ICD10 CODES: T14.91, Z91.5
**Validation:** No validation data | **Condition:** Mental health

**Audit hash:** `db8bc6ae6a31d425...`

#### Extracted Content
```
Suicidal behaviour is an emergency and requires immediate attention. It is an attempted conscious act of self-destruction, which the individual concerned views as the best solution. It is usually associated with feelings of hopelessness, helplessness and conflicts between survival and death.

Self-harm is a broader term referring to intentional poisoning or self-inflicted harm, which may or may not have an intent of fatal outcome.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 9.2.2.2 Suicidal Behaviour/Self Harm ICD10 CODES: T14.91, Z91.5 match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 129. narrative-1385
**Pages:** ? | **Section:** 9.2.2.2 Suicidal Behaviour/Self Harm ICD10 CODES: T14.91, Z91.5
**Validation:** No validation data | **Condition:** Mental health

**Audit hash:** `db8bc6ae6a31d425...`

#### Extracted Content
```
Suicidal behaviour is an emergency and requires immediate attention. It is an attempted conscious act of self-destruction, which the individual concerned views as the best solution. It is usually associated with feelings of hopelessness, helplessness and conflicts between survival and death.

Self-harm is a broader term referring to intentional poisoning or self-inflicted harm, which may or may not have an intent of fatal outcome.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 9.2.2.2 Suicidal Behaviour/Self Harm ICD10 CODES: T14.91, Z91.5 match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 9.2 PSYCHIATRIC AND SUBSTANCE USE DISORDERS > 9.2.1 Anxiety ICD10 CODE: F40-F48

### 127. narrative-1370
**Pages:** ? | **Section:** 9.2.1 Types and clinical features
**Validation:** No validation data | **Condition:** Mental health

**Audit hash:** `226e81a8c0c11bc7...`

#### Extracted Content
```
- ~ Generalized anxiety: Unrealistic and excessive worry about almost everything
- ~ Panic attacks: Episodes of sudden onset of intense apprehension or fear; anxiety symptoms usually peak within 10-15 minutes and resolve in a few minutes to one hour
- ~ Phobia: An excessive fear of a known stimulus (object or
- ~ situation) e.g. animals, water, confined space) causing the person to consciously avoid the object or situation

Each of the above clinical types will have one or more of the following manifestations:

- ~ Sleep, mood and concentration problems
- ~ Palpitations, dizziness, shortness of breath
- ~ Shakiness or tremors, excessive sweatiness
- ~ Easily frightened
- ~ Other symptoms: urinary frequency, hesitancy, or urgency, diarrhoea
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 9.2.1 Types and clinical features match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 128. narrative-1373
**Pages:** ? | **Section:** 9.2.1 Caution
**Validation:** No validation data | **Condition:** Mental health

**Audit hash:** `daff94e29e92178a...`

#### Extracted Content
```
- Diazepam is addictive and abrupt cessation can cause withdrawal symptoms. Use for short periods and gradually reduce the dose. Avoid alcohol
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 9.2.1 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 11.1 BLOOD DISORDERS > 11.1.1 Anaemia > 11.1.1.2 Megaloblastic Anaemia ICD10 CODE: D51-52

### 130. narrative-1506
**Pages:** ? | **Section:** 11.1.1.2 Note
**Validation:** No validation data | **Condition:** Anaemia

**Audit hash:** `d046f61975be2780...`

#### Extracted Content
```
-  If vitamin B12 deficiency is suspected: (low leucocytes and platelets, neuropsychiatric symptoms, vegan diet) DO NOT GIVE folic acid alone but refer for further testing and treatment. Giving folic acid alone in
-  patients with B12 deficiency may precipitate permanent neurological deficit.
-  Anaemia normally corrects within 1-2 months. White cell count and thrombocytopenia normalise within 7-10 days
-  DO NOT use ferrous-folate combination tablets to treat folic deficiency because the quantity of folic acid is too low
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 11.1.1.2 Note match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 11.1 BLOOD DISORDERS > 11.1.1 Anaemia > 11.1.1.3 Normocytic Anaemia

### 131. narrative-1511
**Pages:** ? | **Section:** 11.1.1.3 Prevention/Health Education for Anaemia
**Validation:** No validation data | **Condition:** Anaemia

**Audit hash:** `bb60a9e7d70a4aa7...`

#### Extracted Content
```
Educate the public about:

- ~ The life long effects of anaemia on health, and cognitive development
- ~ Dietary measures: encourage exclusive breastfeeding for the first 6 months. Encourage the use of iron-containing weaning locally available foods (red meat, beans, peas, dark leafy vegetables)
- ~ Hygiene: avoid walking barefeet to avoid hook worm infestation, use of pit latrines for faecal disposal, and practice good hand washing habits
- ~ Medical: encourage periodic screening for children and pregnant mothers, and presumptive iron therapy for either groups in cases of anaemia (see IMCI and pregnancy guidelines, chapters 16 and 17)
- ~ Routine iron supplementation for all pregnant mothers
- ~ Early treatment of malaria, helminthic infections, etc.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.1.1.3 Prevention/Health Education for Anaemia match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 11.1 BLOOD DISORDERS > 11.1.2 Bleeding Disorders

### 132. narrative-1517
**Pages:** ? | **Section:** 11.1.2 Management
**Validation:** No validation data

**Audit hash:** `aff5bf27f35678f9...`

#### Extracted Content
```
-  In patients with ITP, first line treatment is oral prednisolone (0.5-2mg/kg/day). Rituximab and Intravenous Immunoglobulin (IVIG) are second line treatments for ITP, however these should be given by a specialist.
-  Transfuse with platelets if Patient is bleeding (therapeutic transfusion) or prophylactically when platelet count is less than 10,000/µL in patients at high risk of bleeding - e.g., cancer patients.
-  Transfuse with fresh fozenfrozen plasma if bleeding is thought to be due to disorders related to clotting factors
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.1.2 Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 133. narrative-1519
**Pages:** ? | **Section:** 11.1.2 Health education
**Validation:** No validation data

**Audit hash:** `7111bb14f5fb6146...`

#### Extracted Content
```
- ~ Advise the patient with chronic bleeding disorder to:
-  Prevent injury
-  Avoid injections and unnecessary surgery
-  Visit the clinic immediately if symptoms occur
-  Continue all medication as prescribed
- ~ All haemophiliacs should have prophylactic treatment before traumatic procedures, e.g., tooth extractions, or surgery
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.1.2 Health education match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 11.1 BLOOD DISORDERS > 11.1.3 Sickle Cell Disease

### 134. narrative-1525
**Pages:** ? | **Section:** 11.1.3 Management of acute complications
**Validation:** No validation data

**Audit hash:** `9a5cc6d87a3c8977...`

#### Extracted Content
```
Uganda Clinical Guidelines 2023

CHAPTER 11: Blood Diseases and Blood Transfusion Guidelines

583

Uganda Clinical Guidelines 2023

CHAPTER 11: Blood Diseases and Blood Transfusion Guidelines

584

-  And/or ibuprofen 400-600 mg every 6-8 hours
-  Child: 5-10 mg/kg 8 hourly
-  And/or oral diclofenac 50 mg 8 hourly
-  Children only &gt;9 years and &gt;35 kg: 2 mg/kg in 3 divided doses
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.1.3 Management of acute complications match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 135. narrative-1526
**Pages:** ? | **Section:** 11.1.3 If pain not controlled, add:
**Validation:** No validation data

**Audit hash:** `fe89e327853497f2...`

#### Extracted Content
```
-  Codeine 30-60 mg every 6 hours (only in patients &gt;12 years)
-  Or oral tramadol 50-100 mg every 6-8 hours (only in patients &gt;12 years)
-  Or Oral morphine at 0.2-0.4 mg/kg every 4 hours and re-assess pain level

(see section 13.1.2) for thr WHO analgesic Ladder

If pain still not controlled, refer to hospital
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify Level of Care assignments (HOSPITAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 11.1.3 If pain not controlled, add: match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 136. narrative-1527
**Pages:** ? | **Section:** 11.1.3 Painful crisis - hospital management (severe pain)
**Validation:** No validation data

**Audit hash:** `c5dbf1d774d2063c...`

#### Extracted Content
```
- [ ]  IV fluids for rehydration

-  Oxygen, keep oxygen saturation &gt;95%
-  Assess for malaria and other infections
-  Injectable diclofenac
-  Child: 1 mg/kg IM 8 hourly
-  Adult: 50-75 mg IM 8 hourly
-  Morphine oral (see section 13.1.2)
-  Child and Adult: 0.3-0.6 mg/kg per dose and reassess
-  Or Morphine IV
-  Child: 0.1-0.2 mg/kg per dose
-  Adult: 5-10 mg dose and re-assess
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.1.3 Painful crisis - hospital management (severe pain) match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 137. narrative-1528
**Pages:** ? | **Section:** 11.1.3 Note
**Validation:** No validation data

**Audit hash:** `b1796bac47955402...`

#### Extracted Content
```
-  Use of laxative: bisacodyl 2.5 mg to 5 mg orally to prevent constipation due to morphine

HC4

RR

HC4

HC4

HC3

H
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.1.3 Note match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 11.2 Blood And Blood Products > 11.2.1 General Principles of Good Clinical Practice in Transfusion Medicine

### 138. narrative-1534
**Pages:** ? | **Section:** 11.2.1 Do not use blood transfusion to:
**Validation:** No validation data

**Audit hash:** `fd465cb1bfbf78fa...`

#### Extracted Content
```
Obtained from appropriately selected donors (voluntary non-remunerated donors)

Uganda Clinical Guidelines 2023

CHAPTER 11: Blood Diseases and Blood Transfusion Guidelines

589

Uganda Clinical Guidelines 2023

CHAPTER 11: Blood Diseases and Blood Transfusion Guidelines

590

-  Screened for transfusion-transmissible infections (TTIs), namely; HIV, hepatitis B, hepatitis C, and syphilis Tested for compatibility (pre-transfusion) between the donor's red cells and the antibodies in the patient's plasma in accordance with national guidelines
- ~ The mandate to collect blood from donors, and screen it for TTI is reserved for UBTS
- ~ Guidelines and procedures for requesting, administering, and recording blood transfusion should be clearly spelled out, and strictly followed to avoid catastrophic mistakes (see below for)
- ~ Ensure the transfused patient is closely monitored (during and after transfusion) and that there is immediate response if any adverse reactions occur
```

#### Extracted Clinical Flags
- **Special populations:** HIV, hepatitis B, hepatitis C, and syphilis Tested for compatibility (pre-transfusion) between the d

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Special populations: HIV, hepatitis B, hepatitis C, and syphilis Tested for compatibility (pre-transfusion) between the d.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.2.1 Do not use blood transfusion to: match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 11.2 Blood And Blood Products > 11.2.2 Blood and Blood Products: Characteristics and Indications > 11.2.2.1 Whole Blood

### 139. narrative-1536
**Pages:** ? | **Section:** 11.2.2.1 Whole Blood
**Validation:** No validation data

**Audit hash:** `538c1fe1d55df8c7...`

#### Extracted Content
```
- ~ Whole blood provides red blood cells, plasma volume, stable coagulation factors (VII, XI), and others
- ~ May not have enough functional platelets and labile coagulation factors (V and VIII)
- ~ It is also used as a raw material from which other blood components are prepared
- ~ 1 unit of whole blood is about 450 ml of donor blood; obtained from a single donation plus 63 mL of anticoagulant/preservative solution. It is available from HC4 level
- ~ Hct is approximately 35%
- ~ Each unit of blood will raise the HB by about 1g/dl
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.2.2.1 Whole Blood match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 140. narrative-1537
**Pages:** ? | **Section:** 11.2.2.1 Indications
**Validation:** No validation data

**Audit hash:** `a10755e76c1f6119...`

#### Extracted Content
```
- ~ Red blood cell replacement in acute blood loss (haemorrhage) with significant hypovolaemia such as in trauma, surgery, invasive procedures, GIT haemorrhage
- ~ Patients in need of red blood cell transfusion, where red cell concentrates or suspensions are not available (consider adding furosemide to avoid fluid overload)
- ~ Only Specialist Use: exchange transfusion in neonates, using less than 5-day old blood units
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.2.2.1 Indications match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 141. narrative-1539
**Pages:** ? | **Section:** 11.2.2.1 Caution
**Validation:** No validation data

**Audit hash:** `2cf8f5914b5bab25...`

#### Extracted Content
```
- ~ Transfusion must be started within 30 minutes of removal from the refrigerator, and completed within 4 hours of starting
- ~ Storage is 2-6°C in approved blood bank refrigerator with temperature charts and alarm
- ~ WB is contraindicated in severe chronic anaemia and incipient cardiac failure (risk of volume overload)
- ~ Blood should not be warmed (improvised warming method commonly used in health facilities is not necessary)
- ~ The routine use of diuretics (furosemide, or lasix), pre-transfusion is not necessary in most patients. Pre-transfusion diuretics are indicated in known cardiac and renal patients - to prevent circulatory overload.
```

#### Extracted Clinical Flags
- **Contraindications:** severe chronic anaemia and incipient cardiac failure (risk of volume overload)
- ~ Blood should not be warmed (improvised warming method commonly used in health facilities is not necessary)
- ~ The routine use of diuretics (furosemide, or lasix), pre-transfusion is not necessary in most patients

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: severe chronic anaemia and incipient cardiac failure (risk of volume overload)
- ~ Blood should not be warmed (improvised warming method commonly used in health facilities is not necessary)
- ~ The routine use of diuretics (furosemide, or lasix), pre-transfusion is not necessary in most patients.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 11.2.2.1 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 11.2 Blood And Blood Products > 11.2.2 Blood and Blood Products: Characteristics and Indications > 11.2.2.2 Red Cell Concentrates (packed red cells)

### 142. narrative-1540
**Pages:** ? | **Section:** 11.2.2.2 Red Cell Concentrates (packed red cells)
**Validation:** No validation data

**Audit hash:** `ccc26897a4d10ef6...`

#### Extracted Content
```
Red cell concentrates contain red blood cells, suspended in a small amount of plasma and additive solutions (which provides nutrients to the red cells in storage). It is in a form of two, or three pediatric bags,

Uganda Clinical Guidelines 2023

CHAPTER 11: Blood Diseases and Blood Transfusion Guidelines

591

Uganda Clinical Guidelines 2023

CHAPTER 11: Blood Diseases and Blood Transfusion Guidelines

592

each containing 80-150 ml, obtained from a single donation. HCT is approximately 55%. It is available from HC4 level.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.2.2.2 Red Cell Concentrates (packed red cells) match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 11.2 Blood And Blood Products > 11.2.2 Blood and Blood Products: Characteristics and Indications > 11.2.2.3 Clinical Indications for Blood Transfusion

### 143. narrative-1546
**Pages:** ? | **Section:** 11.2.2.3 Severe acute anaemia in children and infants
**Validation:** No validation data

**Audit hash:** `ebbb1d9cf778b6f7...`

#### Extracted Content
```
Transfuse, if;

- ~ Hb ≤ 4 g/dL (or haematocrit ≤ 12%), whatever the clinical condition of the patient
- ~ Hb 4 - 6 g/dL (or haematocrit 13-18%), in case of life threatening complications, such as, clinical features of hypoxia and cardiac decompensation, acidosis (usually causes respiratory distress , impaired consciousness/coma, hyperparasitaemia (&gt;20%) or cerebral malaria, septicaemia,
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.2.2.3 Severe acute anaemia in children and infants match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 11.2 Blood And Blood Products > 11.2.3 Adverse Reactions following Transfusion

### 144. narrative-1560
**Pages:** ? | **Section:** 11.2.3 Key points
**Validation:** No validation data

**Audit hash:** `dc72329eacf22abd...`

#### Extracted Content
```
- ~ Accurate patient identification - at bed side, is critical during;
-  Blood sample collection
- Administration of blood
- ~ Monitoring transfusion is only way to identify ATRs
- ~ Monitoring transfusion is performed by taking vital signs; before, 15 minutes into, whenever a reaction is suspected, and at the end of transfusion
- ~ Vital signs should always be taken (at a minimum) immediately prior to beginning the transfusion, 15 min after start and at end (see box with Key Points). In addition, a nurse or physician should observe the patient for the first 15 minutes after a new blood unit is started, and vital signs recorded
- ~ Errors and failure to follow correct procedures are the most common causes of life threatening acute haemolytic reactions. Such errors include; misidentification of patients - resulting in administering the wrong blood unit to the wrong patient, not repeating blood grouping of the blood units received at hospital, not cross-matching, and errors in labeling blood samples for pre-transfusion grouping and cross-match. These errors must be avoided.
- ~ ALWAYS store blood used for the compatibility testing for 7 days at 2-8°C for possible investigation on transfusion reactions
- ~ In a conscious patient with a severe acute haemolytic transfusion reaction, signs/symptoms may appear within minutes of infusing only 5-10 mL of blood
-  In an unconscious or anaesthetised patient, hypotension, hypoxia and uncontrolled bleeding may be the only signs of a transfusion problem. As such, taking vitals regularly is important.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify Level of Care assignments (HOSPITAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 11.2.3 Key points match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 145. narrative-1561
**Pages:** ? | **Section:** 11.2.3 Vital signs taken;
**Validation:** No validation data

**Audit hash:** `1c0254b7714c59b0...`

#### Extracted Content
```
-  Temperature
-  BP
-  Respiratory rate
-  Pulse rate
- ~ Any unexpected change(s) in vitals = a possible ATR, until proved otherwise

If atransfusion reaction is suspected

-  Stop the transfusion, and remove the giving set. Prior to disconnecting, the unit must be closed to avoid reflux of patient blood into the donor blood

Uganda Clinical Guidelines 2023

CHAPTER 11: Blood Diseases and Blood Transfusion Guidelines

597

Uganda Clinical Guidelines 2023

CHAPTER 11: Blood Diseases and Blood Transfusion Guidelines

598

-  Check the blood pack labels and patient's identity. If there is a discrepancy, consult the blood bank
-  Evaluate the patient; take vitals, and manage accordingly (See table below)
-  Maintain intravenous access
-  Obtain a post-transfusion blood sample. Return the implicated blood unit to the hospital blood bank. Re-grouping and testing are done on both patient and transfused samples
-  Immediately report all suspected acute transfusion reactions to the hospital blood bank laboratory that works with the clinician
-  For category two reactions, record the following in the patient's notes: type of reaction, time reaction occurred from start of transfusion, volume, type, and pack numbers of blood products transfused
-  The type of reaction should be diagnosed, and a quick and clear investigation should be started in the hospital blood bank laboratory
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 11.2.3 Vital signs taken; match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 12.2 Prevention of Cancer

### 146. narrative-1570
**Pages:** ? | **Section:** 12.2 Prevention of Cancer
**Validation:** No validation data | **Condition:** Cancer

**Audit hash:** `986f4309b6a79e36...`

#### Extracted Content
```
Cancer prevention means activities or actions directed at avoiding, reducing, eliminating, or eradicating the risk of developing cancer or the impact of cancer on individuals and populations to promote health.

Approximately 40% of cancers are preventable through interventions such as prevention of oncogenic infections (HPV, HIV, HBV, etc), alcohol, tobacco, and, environmental controls, promotion of healthy diets, and physical activity.

Prevention offers the most cost-effective long-term strategy for control of cancer.

Health workers are responsible for educating the public on:

- ~ Primary Prevention - sustained action to prevent a cancerous process from developing through risk factor reduction
- ~ Secondary Prevention - active discovery and control of cancerous or pre-cancerous lesions
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 12.2 Prevention of Cancer match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 12.2 Prevention of Cancer > 12.2.1 Primary Prevention

### 147. narrative-1571
**Pages:** ? | **Section:** 12.2.1 Primary Prevention
**Validation:** No validation data | **Condition:** Cancer

**Audit hash:** `60fa590892c1f174...`

#### Extracted Content
```
Prevention of cancer includes activities or actions directed at avoiding, reducing, eliminating, or eradicating the risk of developing cancer prior to the onset of cancer.

Uganda Clinical Guidelines 2023

CHAPTER 12: Oncology

605

Uganda Clinical Guidelines 2023

CHAPTER 12: Oncology

606

Primary prevention gives control to the individual in maintaining a healthy lifestyle and environment to avoid or reduce cancer risk.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 12.2.1 Primary Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 12.2 Prevention of Cancer > 12.2.1 Primary Prevention > 12.2.1.1 Control of Risk Factors

### 148. narrative-1572
**Pages:** ? | **Section:** 12.2.1.1 Smoking/Tobacco Use
**Validation:** No validation data | **Condition:** Cancer

**Audit hash:** `107ddb43deb05684...`

#### Extracted Content
```
-  Tobacco use increases the risk of several types of cancer, especially cancer of the lungs, oesophagus, larynx, mouth, throat, kidney, bladder, pancreas, stomach, and cervix
-  Health workers must educate patients / clients / communities on the dangers of tobacco consumption and smoking; patients should be advised to avoid tobacco use. For patients /clients who smoke or use tobacco in any other form, health workers must encourage and support them to stop tobacco use.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 12.2.1.1 Smoking/Tobacco Use match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 149. narrative-1573
**Pages:** ? | **Section:** 12.2.1.1 Unhealthy Diet
**Validation:** No validation data | **Condition:** Cancer

**Audit hash:** `68232104d3a5b6da...`

#### Extracted Content
```
Consumption of unhealthy (unbalanced diet, sweetened food and beverages, charred, and unhygienic food) increases the risk of several types of cancer, especially cancer of the colon and rectum, mouth, pharynx, and larynx, corpus uteri, breast, kidney, liver, pancreas, esophagus, thyroid, prostate, multiple myeloma, and gallbladder.

-  Health workers must educate patients / clients / communities to:
-  balance their diet with various types of healthy foods,
-  eat plenty of healthy food such as whole grains, pulses, fruits, and vegetables,
-  limit food high in sugar or fat and avoid sugary drinks,
-  limit the amount of salt intake,
-  limit eating red meat and avoid eating processed meat,
-  avoid eating burnt or charred food.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 12.2.1.1 Unhealthy Diet match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 150. narrative-1577
**Pages:** ? | **Section:** 12.2.1.1 Environmental Pollution
**Validation:** No validation data | **Condition:** Cancer

**Audit hash:** `0d3b201ae5014b6a...`

#### Extracted Content
```
Regular exposure to carcinogenic chemicals in the environment can occur through unsafe drinking water, air pollution, and food contaminated by aflatoxin or dioxin chemicals, occupational exposure to dangerous gases or dusts.

Environmental carcinogens (aflatoxins, asbestos, vehicle emissions, lead, ultraviolet light, and ionizing radiation) will lead to increased risk of developing cancer, e.g. lung cancer

Health workers must educate patients on environmental dangers and provide suggestions to limit exposure such as:

-  Limiting indoor air pollution due to smoke from use of charcoal

Uganda Clinical Guidelines 2023

CHAPTER 12: Oncology

607

Uganda Clinical Guidelines 2023

CHAPTER 12: Oncology

608

- and firewood inside a poorly ventilated house
-  Avoiding fumes from cars
-  Avoiding exposure to garbage pollution (burning rubbish)
-  Employers should provide employees with a safe working environment with limited occupational hazards
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 12.2.1.1 Environmental Pollution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 151. narrative-1578
**Pages:** ? | **Section:** 12.2.1.1 Oncogenic Infections
**Validation:** No validation data | **Condition:** Cancer

**Audit hash:** `15e111b58b79ba16...`

#### Extracted Content
```
The following infections are associated with causing certain types of cancer:

-  Viral Hepatitis B/C: cancer of the liver
-  Human Papilloma Virus (HPV): cervical, oral, anal, and cancer
-  Helicobacter Pylori: Gastric (stomach) cancer
-  HIV/AIDS: aggressive lymphoma subtypes, Kaposi's sarcoma, anorectal cancer, cervical cancer, etc.
-  Schistosomiasis: increases risk of bladder cancer
-  Liver Fluke: increases risk of cholangio-carcinoma
-  Preventative measures to control oncogenic infection risk include vaccination, and prevention/treatment of infection and infestation:
-  HPV Vaccination: vaccinate all girls aged 10 years with 2 doses of HPV vaccine (for detail see section 18 on immunization)
-  Engage in safe sexual behaviour to avoid sexually transmitted diseases that can cause or increase the risk of certain types of cancer such as cervical, Kaposi sarcoma, lymphoma, and liver cancers.
-  Hepatitis B Vaccination: routinely offered in the national childhood schedule and populations at risk, in order to prevent infection with hepatitis B, the main risk factor for liver cancer (for detail see section 18 on immunization)
-  Treatment of HIV/AIDS, schistosomiasis, H. pylori, and hepatitis B&amp;C and other infections is also a preventive measure.
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 12.2.1.1 Oncogenic Infections match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 12.2 Prevention of Cancer > 12.2.2 Secondary Prevention

### 152. narrative-1581
**Pages:** ? | **Section:** 12.2.2 Secondary Prevention
**Validation:** No validation data | **Condition:** Cancer

**Audit hash:** `a7c06b5879f7ad5d...`

#### Extracted Content
```
Secondary prevention of cancer includes activities or actions directed at halting the progress of cancer at its incipient stage through screen-

Uganda Clinical Guidelines 2023

CHAPTER 12: Oncology

609

Uganda Clinical Guidelines 2023

CHAPTER 12: Oncology

610

ing, early diagnosis, pre-cancer treatment or cancer management, and referral to avoid or reduce complications associated with the cancer. Secondary prevention strategies relate to the discovery and control of cancerous or pre-cancerous lesions.

Early detection of cancer greatly increases the chances for successful treatment and cure. It comprises of:

- ~ Early diagnosis in symptomatic populations
- ~ Screening in asymptomatic high-risk populations

Screening refers to the use of simple tests across a healthy population in order to identify individuals who have disease, but do not yet have symptoms.

Based on existing evidence, mass population screening is advocated for breast and cervical cancer. Other cancers that are commonly screened for include prostate and colorectal cancers
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 12.2.2 Secondary Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 153. narrative-1582
**Pages:** ? | **Section:** 12.2.2 Screening for Breast Cancer
**Validation:** No validation data | **Condition:** Cancer

**Audit hash:** `2cb74b7aef3d024b...`

#### Extracted Content
```
Screening / health checkup for breast cancer involves:

Breast Self-Examination (BSE): a simple, quick examination done by the client herself, aimed at early detection of lumps. Regular (monthly-not during menstruation, at least seven days after ending the menstruation) and correct technique of breast examination is important and easy to teach and administer. Health workers should note that BSE is not a standard screening test for breast cancer, but is beneficial for breast health awareness.

Clinical Breast Examination (CBE): performed by a trained and skilled health care provider from HC3

-  Take a detailed history and conduct a physical
- examination
-  Inspect the skin for changes and swellings, for tethering of
-  All breast quadrants must be examined in detail plus the armpits for lymph nodes
-  the breast on the chest wall, palpate for lumps, check for nipple discharge
-  A suspicious lump or bloody nipple discharge MUST BE REFERRED for evaluation by mammography or ultrasonography as well as core needle biopsy

Mammography: a low-dose x-ray of the breast is the test of choice for screening of early breast cancer but it is available only at national referral hospital level.

Breast Ultrasound: not used as a screening test, but is useful as an additional tool in characterizing palpable tumors and taking of im age-directed biopsies. It may be used as a screening tool in lactating women, small- breasted women and in males, and as diagnostic tests in symptomatic patients.
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify Level of Care assignments (HC3, HOSPITAL, NATIONALREFERRAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 12.2.2 Screening for Breast Cancer match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 12.3 Common Cancers

### 154. narrative-1585
**Pages:** ? | **Section:** 12.3 Common Cancers
**Validation:** No validation data | **Condition:** Cancer

**Audit hash:** `b1d7666cbe848cb9...`

#### Extracted Content
```
This section describes the signs and symptoms of common cancers in adults and children, and outline some of the investigations required. Health workers should suspect cancer if they observe any of these clinical features and refer patients to the cancer treatment centers (Uganda Cancer Institte and regional referral hospitals).
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify Level of Care assignments (HOSPITAL, REGIONALREFERRAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 12.3 Common Cancers match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 13.2 OTHER CONDITIONS IN PALLIATIVE CARE > 13.2.9 End of Life Care

### 155. narrative-1632
**Pages:** ? | **Section:** 13.2.9 Investigations
**Validation:** No validation data

**Audit hash:** `eda1610fa0271a22...`

#### Extracted Content
```
-  Exclude reversible problems (e.g. drug toxicity, infections, dehydration, biochemical abnormalities)
-  It is important to weigh the benefit versus the burden in assessing an intervention, and/or management plan based on the clinical features exhibited by the patient
-  Before ordering a test, always ask "will this test change my management plan or the outcome for the patient?"
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 13.2.9 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 13.2 OTHER CONDITIONS IN PALLIATIVE CARE > 14.1.2 Pelvic Inflammatory Disease (PID) ICD10 CODE: N70-N73

### 156. narrative-1648
**Pages:** ? | **Section:** 14.1.2 Notes
**Validation:** No validation data

**Audit hash:** `bb82bbac8d904569...`

#### Extracted Content
```
-  All women with PID should be tested for HIV
-  Abstain from sex or use barrier methods during the course of treatment
-  Do not take alcohol when taking metronidazole
-  Avoid sex during menstrual period and for 6 weeks after an abortion
-  In IUD users with PID, the IUD need not be removed. However, if there is no clinical improvement within 48-72 hours of initiating treatment, providers should consider removing the IUD and help patient choose an alternative contraceptive method (see chapter 15)
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 14.1.2 Notes match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 15.1 Key steps to be followed in provision of fp services Icd10 code: z10.0 > 15.1.10 Summary of Medical Eligibility for Contraceptives

### 157. narrative-1679
**Pages:** ? | **Section:** 15.1.10 Methods all couples (except a few) can safely use
**Validation:** No validation data

**Audit hash:** `6d1cb63af399df00...`

#### Extracted Content
```
Emergency contraceptive pill (for emergency use only) Bilateral Tubal Ligation (BTL) and Vasectomy

Barrier methods (condoms, diaphragm) Lactational amenorrhoea method (LAM)

Fertility awareness (FAM) and Standard days methods
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 15.1.10 Methods all couples (except a few) can safely use match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 15.2 Overview Of Key Contraceptive Methods > 15.2.5 Injectable Progestogen-Only Contraceptive

### 158. narrative-1727
**Pages:** ? | **Section:** 15.2.5 If irregular bleeding continues, immediately:
**Validation:** No validation data

**Audit hash:** `2de0aa82c1ef303d...`

#### Extracted Content
```
- [ ]  Give 400-800 mg ibuprofen 8 hourly when irregular bleeding starts

-  Or 500 mg mefenamic acid eight hourly after meals for five days

Avoid Tranexamic acid for treatment of bleeding as a result of using contraceptives for fear of blood clots .

- ~ If irregular bleeding continues or starts after several months of normal or no monthly bleeding:
- ~ Investigate other reasons (unrelated to the contraceptive) and treat accordingly
- ~ Help client choose another FP method if necessary
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 15.2.5 If irregular bleeding continues, immediately: match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 15.2 Overview Of Key Contraceptive Methods > 15.2.7 Emergency Contraception (Pill and IUD)

### 159. narrative-1752
**Pages:** ? | **Section:** 15.2.7 Emergency Contraception (Pill and IUD)
**Validation:** No validation data

**Audit hash:** `8727cbf61e0216fc...`

#### Extracted Content
```
ICD10 CODE: Z30.012

Emergency Contraception can be used to prevent unwanted pregnancy after unprotected sex, rape, defilement or contraceptive method failure. Methods available include Emergency Contraceptive Pills and IUDs.

Caution: Emergency contraceptive methods do not cause abortion.

Regular Emergency Contraceptive Pill users should be counselled to use routine contraceptive method.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 15.2.7 Emergency Contraception (Pill and IUD) match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 160. narrative-1755
**Pages:** ? | **Section:** 15.2.7 Advantages
**Validation:** No validation data

**Audit hash:** `9980382141f2c926...`

#### Extracted Content
```
- ~ Prevents unplanned pregnancy after penetrative sexual intercourse
- ~ Safe for all women and have no long-term side effects
- ~ Do not cause infertility
- ~ Able to have on hand in case of emergency
- ~ Controlled by the woman
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 15.2.7 Advantages match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 15.2 Overview Of Key Contraceptive Methods > 15.2.8 Intrauterine Device (IUD)

### 161. narrative-1760
**Pages:** ? | **Section:** 15.2.8 Indications
**Validation:** No validation data

**Audit hash:** `57e75b191f3cda79...`

#### Extracted Content
```
- ~ Women desiring long-term contraception
- ~ Breastfeeding mothers
- ~ When hormonal FP methods are contraindicated
- ~ Treatment of heavy periods- menorrhagia (for levonorgestrel)
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 15.2.8 Indications match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 162. narrative-1762
**Pages:** ? | **Section:** 15.2.8 Advantages
**Validation:** No validation data

**Audit hash:** `d5e5dbd3adfe9db0...`

#### Extracted Content
```
Prevents unplanned pregnancy after penetrative sexual intercourse

Uganda Clinical Guidelines 2023

CHAPTER 15: Family Planning (FP)

685

Uganda Clinical Guidelines 2023

CHAPTER 15: Family Planning (FP)

686

- ~ Can be used as an emergency
- ~ Safe for all women including breast feeding mothers
- ~ Does not affect libido (copper)
- ~ Long term
- ~ 97-99% effective
- ~ Reduces chances of getting STIs (Lenovorgestrel)
- ~ It's recommended for women with NCDs like diabetes, hypertension
- ~ Does not increase the risk of STIs
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 15.2.8 Advantages match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 15.2 Overview Of Key Contraceptive Methods > 15.2.9 Natural FP: Cervical Mucus Method (CMM) and Moon Beads ICD10 CODE: Z30.02

### 163. narrative-1771
**Pages:** ? | **Section:** 15.2.9 Natural FP: Cervical Mucus Method (CMM) and Moon Beads ICD10 CODE: Z30.02
**Validation:** No validation data

**Audit hash:** `89fd4dc56cf7bb7a...`

#### Extracted Content
```
CMM is a fertility awareness-based method of FP which relies on the change in the nature of vaginal mucus during the menstrual cycle in order to detect the fertile time. During this time, the couple avoidspregnancy by changing sexual behaviour as follows:

- ~ Abstaining from sexual intercourse: Avoiding vaginal sex completely (also called periodic abstinence)
- ~ Using barriers methods, e.g., condoms, cervical caps
- ~ Guidance on correct use of the method is only available at centres with specially trained service providers.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 15.2.9 Natural FP: Cervical Mucus Method (CMM) and Moon Beads ICD10 CODE: Z30.02 match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.1 ANTENATAL CARE (ANC) ICD10 CODE: Z36

### 164. narrative-1780
**Pages:** ? | **Section:** 16.1 ANTENATAL CARE (ANC) ICD10 CODE: Z36
**Validation:** No validation data

**Audit hash:** `3ac5c3ea92acc361...`

#### Extracted Content
```
Antenatal care is a planned programme of medical care offered to pregnant women by a skilled birth attendant, from the time of conception to delivery, aimed at ensuring a safe and satisfying pregnancy and birth outcome.

The main objective of antenatal care is to give information on:

- ~ Screening, prevention, and treatment of complications
- ~ Emergency preparedness
- ~ Birth planning
- ~ Satisfying any unmet nutritional, social, emotional, and physical needs of the pregnant woman
- ~ Provision of patient education, including successful care and nutrition of the newborn
- ~ Identification of high-risk pregnancy
- ~ Encouragement of male partner involvement in antenatal care
```

#### Extracted Clinical Flags
- **Special populations:** pregnant women by a skilled birth attendant, from the time of conception to delivery, aimed at ensur

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.1 ANTENATAL CARE (ANC) ICD10 CODE: Z36 match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.1 ANTENATAL CARE (ANC) ICD10 CODE: Z36 > 16.1.3 High Risk Pregnancy (HRP)

### 165. narrative-1787
**Pages:** ? | **Section:** 16.1.3 Management
**Validation:** No validation data | **Condition:** Maternal health

**Audit hash:** `2b3a85e0da6ce1f8...`

#### Extracted Content
```
Note : Skilled attendance at birth remains the most important component of comprehensive emergency obstetric and new-born care.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.1.3 Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.2 MANAGEMENT OF SELECTED CONDITIONS IN PREGNANCY > 16.2.2 Pregnancy and HIV Infection > 16.2.2.1 Care for HIV Positive Women (eMTCT) ICD10 CODE: 098.719

### 166. narrative-1798
**Pages:** ? | **Section:** 16.2.2.1 During labour: safe obstetric practices
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `c12b577a535adb91...`

#### Extracted Content
```
-  Avoid episiotomy
- Avoid artifical rupture of membranes
-  Avoid instrumental delivery (vacuum)
- Avoid frequent vaginal examination
-  Do not milk umbilical cord before cutting
- Actively manage third stage of labour
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 16.2.2.1 During labour: safe obstetric practices match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 167. narrative-1801
**Pages:** ? | **Section:** 16.2.2.1 Caution
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `0445f8f8ca68b493...`

#### Extracted Content
```
-  In case of low body weight, high creatinine, diabetes, hypertension, chronic renal disease, and concomitant nephrotoxic medications: perform renal investigation before giving TDF

HC3

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

705

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

706

-  TDF is contraindicated in advanced chronic renal disease
```

#### Extracted Clinical Flags
- **Contraindications:** advanced chronic renal disease

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: advanced chronic renal disease.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 16.2.2.1 Caution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.2 MANAGEMENT OF SELECTED CONDITIONS IN PREGNANCY > 16.2.2 Pregnancy and HIV Infection > 16.2.2.2 Counselling for HIV Positive Mothers

### 168. narrative-1803
**Pages:** ? | **Section:** 16.2.2.2 Counselling for HIV Positive Mothers
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `b48b7b9d2b4080b8...`

#### Extracted Content
```
- ~ Give psychosocial support
- ~ Encourage mothers to enroll in Family Support Groups (FSG) for peer support
- ~ Advise on the importance of good nutrition
-  Talk to family members to encourage the woman to eat enough and help her avoid hard physical work
-  Micronutrient supplementation during pregnancy and
- breastfeeding; iron + folic acid and multivitamins
- ~ Advise her that she is more liable to infections, and to seek medical help as soon as possible
- ~ Review the birth plan
-  Advise her to continue attending ANC
- Advise her to deliver in a health facility where appropriate care can be provided for her and the baby
- starts or membranes rupture
-  Advise her to go to the health facility as soon as labour
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 16.2.2.2 Counselling for HIV Positive Mothers match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 169. narrative-1804
**Pages:** ? | **Section:** 16.2.2.2 During postpartum period
**Validation:** No validation data | **Condition:** HIV/AIDS

**Audit hash:** `02b6d6c51dd73866...`

#### Extracted Content
```
- ~ Advise on the infectiousness of lochia and blood- stained sanitary pads, and how to dispose them off safely according to local facilities
- ~ If not breastfeeding exclusively, advise her to use a family planning method immediately to prevent unwanted pregnancy
- ~ Linkage of mother-baby pair and her family, for on-going care beyond peurperium
- ~ Breast care: If not breastfeeding, advise that:
-  The breasts may be uncomfortable for a while
-  She should avoid expressing the breast to remove milk (the more you remove the more it forms)
-  She should support her breasts with a firm, well-fitting
-  bra or cloth, and give her paracetamol for painful breasts
-  Advise her to seek care if breasts become painful,
-  swollen, red; if she feels ill; or has fever
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 16.2.2.2 During postpartum period match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.3 ANTENATAL COMPLICATIONS > 16.3.3 Ectopic Pregnancy

### 170. narrative-1833
**Pages:** ? | **Section:** 16.3.3 Ectopic Pregnancy
**Validation:** No validation data | **Condition:** Maternal health

**Audit hash:** `c669285cc4217e6c...`

#### Extracted Content
```
ICD10 CODE: O00

Pregnancy outside the uterus, usually in the uterine tubes; could result in an emergency when the tube ruptures
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.3.3 Ectopic Pregnancy match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.3 ANTENATAL COMPLICATIONS > 16.3.6 Antepartum Haemorrhage (APH) - Abruptio Placentae and Placenta Praevia ICD10 CODE: O44-O46

### 171. narrative-1856
**Pages:** ? | **Section:** 16.3.6 Investigations
**Validation:** No validation data

**Audit hash:** `447d49069d3381ff...`

#### Extracted Content
```
-  In case of Abruptio Placentae where the baby is alive
- -Deliver by emergency caesarean section (ensure
- -you have enough blood)
-  In case of placenta praevia
- -Give steroids (as for PPROM) if &lt;34 weeks
- -Emergency cesarean section if bleeding is uncontrolled, mother's or baby's life in danger or pregnancy &gt;37 weeks
- -If bleeding resolves, keep mother in hospital and
- -deliver at &gt;37 weeks
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify Level of Care assignments (HOSPITAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.3.6 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.3 ANTENATAL COMPLICATIONS > 16.3.7 Pre-Eclampsia

### 172. narrative-1861
**Pages:** ? | **Section:** 16.3.7 Management
**Validation:** No validation data

**Audit hash:** `3acc0d5af5d24f9e...`

#### Extracted Content
```
Any case of pre-eclampsia has to be referred to hospital, lower facilities can give emergency care (Magnesium sulphate, antihypertensive as available).
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify Level of Care assignments (HOSPITAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.3.7 Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.3 ANTENATAL COMPLICATIONS > 16.3.8 Eclampsia

### 173. narrative-1866
**Pages:** ? | **Section:** 16.3.8 Clinical features
**Validation:** No validation data

**Audit hash:** `35f71ed32aaef7c3...`

#### Extracted Content
```
-  Patient may or may not have had previous clinical features of severe pre-eclampsia
-  Headache that is usually frontal, blurring of vision, aura (flickering lights)
-  Generalized tonic-clonic seizures
-  Right upper quadrant abdominal pain with nausea
-  BP raised &gt;140/90 mmHg
-  Oedema of legs and sometimes face and body
-  Unconsciousness if condition not treated
-  Amnesia and other mental changes
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.3.8 Clinical features match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 174. narrative-1869
**Pages:** ? | **Section:** 16.3.8 Principles of Management
**Validation:** No validation data

**Audit hash:** `950898b42e484fb0...`

#### Extracted Content
```
Eclampsia is a medical emergency and should be referred to hospital urgently, after first aid measures as available.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify Level of Care assignments (HOSPITAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.3.8 Principles of Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.4 LABOUR, DELIVERY AND ACUTE COMPLICATIONS > 16.4.1 Normal Labour and Delivery

### 175. narrative-1876
**Pages:** ? | **Section:** 16.4.1 Hydration and nourishment
**Validation:** No validation data

**Audit hash:** `2d0ef883a46c0989...`

#### Extracted Content
```
-  Ensure oral or IV fluid intake especially in prolonged labour, to avoid dehydration and ketosis
-  Give normal saline and Dextrose solution as required
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 16.4.1 Hydration and nourishment match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.4 LABOUR, DELIVERY AND ACUTE COMPLICATIONS > 16.4.2 Induction of Labour

### 176. narrative-1883
**Pages:** ? | **Section:** 16.4.2 Induction of Labour
**Validation:** No validation data

**Audit hash:** `d93a7efcec433bc3...`

#### Extracted Content
```
Induction of labour may be indicated for medical reasons, like, pre-eclampsia, diabetes, post-term pregnancy.

However, possible risks of induction are:



Failed induction



Hyperstimulation syndrome, requiring emergency caesarean section.

Induction is contraindicated in para 5 and above and in patients with a previous scar. In these cases there is indication for caesarean section.
```

#### Extracted Clinical Flags
- **Contraindications:** para 5 and above and in patients with a previous scar

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: para 5 and above and in patients with a previous scar.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.4.2 Induction of Labour match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.4 LABOUR, DELIVERY AND ACUTE COMPLICATIONS > 16.4.5 Retained Placenta

### 177. narrative-1901
**Pages:** ? | **Section:** 16.4.5 Management
**Validation:** No validation data

**Audit hash:** `cc957ed243f216d6...`

#### Extracted Content
```
16.4.6 Postpartum Haemorrhage (PPH) ICD10 CODE: O72

Vaginal bleeding of more than 500 mL after vaginal delivery or &gt;1000 mL after caesarean section.

- -Primary PPH occurs in the first 24 hours after delivery
- -Secondary PPH occurs between 24 hours and six weeks after delivery

PPH is an EMERGENCY. It can occur in any woman and needs prompt recognition and treatment.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.4.5 Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.4 LABOUR, DELIVERY AND ACUTE COMPLICATIONS > 16.4.8 Care of Mother and Baby Immediately After Delivery ICD10 CODE: Z39 > 16.4.8.1 Care of Mother Immediately After Delivery

### 178. narrative-1919
**Pages:** ? | **Section:** 16.4.8.1 Breastfeeding
**Validation:** No validation data

**Audit hash:** `e7efc4b9b27089f4...`

#### Extracted Content
```
Ensure the mother starts breastfeeding as soon as possible (preferably within the first hour)

-  Offer mother help to position (attach) the baby correctly onto the breast to avoid cracked nipples
-  Counsel and reassure mother
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.4.8.1 Breastfeeding match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 179. narrative-1920
**Pages:** ? | **Section:** 16.4.8.1 If unable to start breastfeeding:
**Validation:** No validation data

**Audit hash:** `f1dda6d475899cd7...`

#### Extracted Content
```
-  Plan for alternative feeding method
- -Ensure that alternative method is Affordable, Feasible, Acceptable, Sustainable and Safe
- -Do not give artificial feeds, sugar water or local feeds
- -before baby has attempted to initiate natural breastfeeding
- -Consider referral to a higher level
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.4.8.1 If unable to start breastfeeding: match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.6 POSTPARTUM CONDITIONS > 16.6.1 Postpartum Care ICD10 CODE: Z39 > 16.6.1.1 Postpartum Counselling

### 180. narrative-1936
**Pages:** ? | **Section:** 16.6.1.1 General counselling
**Validation:** No validation data

**Audit hash:** `30a4d9e84aea055e...`

#### Extracted Content
```
-  Breastfeeding/breast care
-  Nutrition, ferrous and folic acid supplements, avoid alcohol and tobacco
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 16.6.1.1 General counselling match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 181. narrative-1937
**Pages:** ? | **Section:** 16.6.1.1 Complications and danger signs for the mother
**Validation:** No validation data

**Audit hash:** `e301fde1f2ea733e...`

#### Extracted Content
```
-  Danger signs (see next table)
-  Readiness plan in case of an emergency
- -Advise her to have someone near for at least 24 hours after delivery to respond to any change in condition
- Where to go if danger signs appear, how to get there, costs involved, family/community support
- -Discuss emergency issues with her and partner/family:
- -Advise her to seek help from the community if needed
- Advise her to bring any home-based maternal record to the health facility, even for an emergency visit
-  Self care and other good health practices, personal hygiene, handwashing, genital hygiene (care of the episiotomy or repaired tears)
-  Pelvic floor exercises
-  Sleeping under mosquito nets
-  Postpartum checks (6 days and 6 weeks)
-  Provide information on bonding by encouraging the mother to hold, touch, explore her baby as well as rooming-in (mother and baby sleeping in the same bedHIV testing
-  Discuss with the couple the need for shared care of the newborn
-  Help build confidence by providing reassurance that the woman is capable of caring for the newborn

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

765

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

766
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.6.1.1 Complications and danger signs for the mother match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 182. narrative-1938
**Pages:** ? | **Section:** 16.6.1.1 Counselling on baby care
**Validation:** No validation data

**Audit hash:** `25f6fced47378d92...`

#### Extracted Content
```
-  Hygiene and care of the baby, (see previous sections)
-  Danger signs for the baby
-  Immunization schedule
-  Let baby sleep on the back or side
-  Ensure the baby is kept warm without overcovering
-  Apply chlorhexidine digluconate gel to the cord stump daily after every bath until the cord falls off. Provide the gel to the mother, and teach her how to use it while at home
-  Keep baby away from smoke and smokers
-  Keep baby (especially if small) away from anyone whois ill
-  Do not share supplies (for example, clothing, feeding utensils) with other babies
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.6.1.1 Counselling on baby care match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.6 POSTPARTUM CONDITIONS > 16.6.4 Obstetric Fistula

### 183. narrative-1967
**Pages:** ? | **Section:** 16.6.4 Predisposing factors
**Validation:** No validation data | **Condition:** Maternal health

**Audit hash:** `e0efd906d6c4ed7f...`

#### Extracted Content
```
-  Lack of access to maternity care
-  Lack of/inadequate skilled care at birth
-  Lack of facilities for ANC and childbirth
-  Lack of knowledge to identify danger signs and promptly respond
-  Poverty and lack of women empowerment
-  Early marriage and childbirth
-  Inadequate family planning access
-  Harmful traditional practices such as Female Genital Mutilation
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.6.4 Predisposing factors match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 184. narrative-1974
**Pages:** ? | **Section:** 16.6.4 Prevention
**Validation:** No validation data | **Condition:** Maternal health

**Audit hash:** `db802817b74e3a64...`

#### Extracted Content
```
-  Provide skilled attendance at births and improve on emergency obstetric care at all levels
-  Increase access to accurate and quality family planning information and services, especially for adolescents
-  Establish appropriate and effective referral system at all levels (early referrals)

ENSURE ALL WOMEN WHO HAVE SUFFERED OBSTRUCTED LABOUR ARE MANAGED ACCORDING TO THE STANDARD MANAGEMENT PROTOCOL FOR FISTULA PREVENTION

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

787

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

788
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.6.4 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 16.7 INTRAUTERINE FETAL DEMISE (IUFD) OR FETAL DEATH IN UTERO (FDIU)

### 185. narrative-1980
**Pages:** ? | **Section:** 16.7 Medical management of IUFD ( ≥ 14 to ≤ 28 weeks)
**Validation:** No validation data

**Audit hash:** `1627fb482aa62853...`

#### Extracted Content
```
-  IUFD may be managed expectantly or treated surgically (D&amp;E) or medically (with medications).
-  Discussions aim to foster shared decision making about the plan for care and support maternal/parental choice.
-  Supportive social and psychological care should be made available to all bereaved parents
-  a combination of mifepristone and misoprostol should be the first-line intervention:

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

789

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

790

- · Mifepristone (200mg) administered orally followed 1-2 days later by repeat doses of 400 µg misoprostol administered sublingually or vaginally every 4-6 hours. The minimum recommended interval between use of mifepristone and misoprostol is 24 hours. Between 24 and 48 hours of mifepristone (200mg), the four tablets of misoprostol should be given vaginally, sublingually and can be administered by physician, midwife or woman herself.
- · Alternative regimens: repeat doses of 400 µg misoprostol administered sublingually or vaginally every 4-6 hours. However, research shows that the combination regimen, above is more effective than misoprostol alone.
-  Expectant Management of IUFD involves awaiting spontaneous labour (may take up to 3 weeks).
-  Recommendations about labour and birth should take into account the mother's preferences, her medical condition and previous intra-partum history.
-  Vaginal birth is the recommended mode of delivery for most women, but caesarean birth may need to be considered in individual cases.
-  Pregnancy tissue should be treated in the same way as other biological material unless the individual expresses a desire for it to be managed otherwise.
-  If a woman has had a previous caesarean section, a discussion as to the safety and benefits of induction of labour needs to be undertaken by a consultant obstetrician.
-  Clinical assessment and evaluation are recommended to assess maternal wellbeing and to determine the cause of death, the chance of recurrence, and of avoiding future pregnancy complications.
-  Laboratory tests are recommended to rule out any maternal disease or risk factor that may have contributed to the IUFD
-  Fetal karyotyping should be considered in all cases.
-  Parents should be offered a full postmortem examination of the baby.
-  Postmortem examination should include external examination with birth weight, histology of relevant tissues and plain radiography (skeletal survey)
-  Pathological examination of the cord, membranes and placenta is recommended in all cases of IUFD
-  Standardized checklists should be used to ensure that all appropriate care options are offered and that each response mark is recorded.
-  A standardized dataset should be collected for all IUFDs.
-  All IUFDs should be reviewed in a multi-professional meeting using a standardized approach.
-  All term intra-partum deaths with no evidence of a major congenital anomaly should be investigated locally.
-  Staff working with bereaved parents should be provided with an opportunity to develop their knowledge and understanding of perinatal loss, together with the development of skills in working in this area.
-  A system should be in place to give clinical and psychological support to staff involved with an IUFD.
-  A follow-up appointment with the consultant obstetrician should be arranged and it should be clear who is responsible for making these arrangements.
-  Women with a history of IUFD should attend a consultant-led hospital-based antenatal clinic in their next pregnancy and undergo increased antenatal surveillance.

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

791

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

792
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify Level of Care assignments (HOSPITAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.7 Medical management of IUFD ( ≥ 14 to ≤ 28 weeks) match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 186. narrative-1981
**Pages:** ? | **Section:** 16.7 NOTE
**Validation:** No validation data

**Audit hash:** `b4ece197de75f6bd...`

#### Extracted Content
```
Medical management of IUFD with mifepristone and misoprostol combined is contraindicated in any person with a known allergy to either medication, ectopic pregnancy, chronic adrenal failure, or inherited porphyria, and used with caution in women with life-threatening un-stabilized conditions such as uncontrolled cardiac disease, severe anemia, or hemorrhagic disorders, uncontrolled serious asthma or in those with an IUD in place.
```

#### Extracted Clinical Flags
- **Contraindications:** any person with a known allergy to either medication, ectopic pregnancy, chronic adrenal failure, or inherited porphyria, and used with caution in women with life-threatening un-stabilized conditions such as uncontrolled cardiac disease, severe anemia, or hemorrhagic disorders, uncontrolled serious asthma or in those with an IUD in place

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: any person with a known allergy to either medication, ectopic pregnancy, chronic adrenal failure, or inherited porphyria, and used with caution in women with life-threatening un-stabilized conditions such as uncontrolled cardiac disease, severe anemia, or hemorrhagic disorders, uncontrolled serious asthma or in those with an IUD in place.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.7 NOTE match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 187. narrative-1989
**Pages:** ? | **Section:** 16.7 Precaution
**Validation:** No validation data

**Audit hash:** `a0d8c8356a90516e...`

#### Extracted Content
```
-  Ectopic pregnancy should be excluded, and intra-uterine gestation confirmed before the medical abortion. The medical abortion regimen will not terminate the ectopic pregnancy
-  Fertility can return within two weeks therefore all patients should be given post-abortion contraception where eligible
-  Access to appropriate medical care must be assured in case an emergency develops; the patient should be given clear verbal and written instructions on whom she should contact and where to go in case of concerns or suspected complications

This chapter presents the management of sick infant and child up to age 5, following the WHO syndromic approach IMNCI.

Additional information about management of childhood illnesses can be found in specific sections:
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 16.7 Precaution match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 17.2 SICK YOUNG INFANT AGE UP TO 2 MONTHS

### 188. narrative-2003
**Pages:** ? | **Section:** 17.2 Counsel the mother on
**Validation:** No validation data

**Audit hash:** `c32e342156ac7d3b...`

#### Extracted Content
```
- [ ]  Nutrition and breastfeeding of the child

-  Her own health needs
-  To return for FOLLOW UP as scheduled
-  To return immediately at the clinic if the danger signs in the table below appear:
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 17.2 Counsel the mother on match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 17.3 SICK CHILD AGE 2 MONTHS TO 5 YEARS

### 189. narrative-2027
**Pages:** ? | **Section:** 17.3 In assessing a sick child, assess for the following:
**Validation:** No validation data

**Audit hash:** `966a2094e625ae57...`

#### Extracted Content
```
- -General danger signs: URGENT ATTENTION and ACTION REQUIRED.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 17.3 In assessing a sick child, assess for the following: match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 190. narrative-2029
**Pages:** ? | **Section:** 17.3 Then counsel the mother on
**Validation:** No validation data

**Audit hash:** `7ad79e2f5045311e...`

#### Extracted Content
```
- -Extra fluids for any sick child
- -Nutrition and breastfeeding of the child
- -How to give home treatments
- -Her own health needs
- -To return for FOLLOW UP as scheduled
-  To return immediately if any danger sign appear
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 17.3 Then counsel the mother on match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 17.3 SICK CHILD AGE 2 MONTHS TO 5 YEARS > 17.3.6 Check for Malnutrition and Feeding Problems

### 191. narrative-2049
**Pages:** ? | **Section:** 17.3.6 Look and feel
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `3bee9f7160846a37...`

#### Extracted Content
```
- ~ Look for signs of acute malnutrition like
- -Oedema on both feet
- -Determine weight for height/ length (WFH/L) using WHO growth charts standards (see end of this chapter)
- -As an alternative, determine weight for age (WFA) using WHO growth chart standard
- -Measure MUAC (Mid Upper Arm Circumference) in children ³ 6 months using MUAC tape

If WFH/L is less than -3 z-scores or MUAC &lt; 115 mm, then

- ~ Check for any medical complication present
- -Any general danger sign
- -Any severe classification
- -Pneumonia or chest indrawing

If no medical complication presents,

- ~ Child ³ 6 months: assess child appetite
- -offer RUTF (Ready to Use Therapeutic Food) and assess if child able to finish the portion or not
- ~ Child £ 6 month: assess breastfeeding
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 17.3.6 Look and feel match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 17.4 INTEGRATED COMMUNITY CASE MANAGEMENT

### 192. narrative-2081
**Pages:** ? | **Section:** 17.4 INTEGRATED COMMUNITY CASE MANAGEMENT
**Validation:** No validation data

**Audit hash:** `477963cd0e1eac48...`

#### Extracted Content
```
Integrated Community Case Management (iCCM) of malaria, pneumonia and diarrhoea is a recently adopted strategy for the treatment of common childhood illness at community level by trained Community Health Workers since 2010. It addresses a gap in delivery of curative services to children below 5 years allowing:

-  prompt and accessible treatment of uncomplicated malaria, pneumonia and diarrhoea
-  identification of danger signs (convulsions, chest in-
-  drawing, unable to feed, vomiting everything, lethargy/ unconsciousness) and pre-referral treatment
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 17.4 INTEGRATED COMMUNITY CASE MANAGEMENT match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 17.5 CHILD GROWTH WEIGHT STANDARDS CHARTS

### 193. narrative-2087
**Pages:** ? | **Section:** 17.5 Weight-for-Age
**Validation:** No validation data

**Audit hash:** `1e6c4f3b08c1e5ab...`

#### Extracted Content
```
Used to show if a child is normal weight or underweight for their age. It should not be used to assess obesity and overweight.
```

#### Extracted Clinical Flags
- **Contraindications:** assess obesity and overweight

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: assess obesity and overweight.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 17.5 Weight-for-Age match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 18.1 ROUTINE CHILDHOOD VACCINATION > 18.1.1 National Immunization Schedule

### 194. narrative-2101
**Pages:** ? | **Section:** 18.1.1 General principles of routine childhood immunization
**Validation:** No validation data

**Audit hash:** `ecb7cc95127d9653...`

#### Extracted Content
```
- ~ The aim is to ensure that all target age groups complete their immunization schedule as above
- ~ Age for vaccinations: Give each vaccine at the recommended age or if this is not possible, at any first contact with the child after this age
- ~ BCG vaccination
- -Give this as early as possible in life, preferably at birth
- Do NOT give BCG vaccine to any child with clinical signs and symptoms of immunosuppression, e.g. AIDS
- ~ Use each vaccine with its corresponding pre-cooled diluent from the same manufacturer
- ~ Polio vaccination (= 'birth dose'): This is a primer dose of oral polio vaccine (OPV), which should be given ideally at birth but otherwise in the first 2 weeks of life
- ~ DPT-HepB-Hib vaccine
- -Is a combination of DPT vaccine + hepatitis B vaccine (HepB) + haemophilus influenzae type b (Hib) vaccine
- ~ Measles rubella vaccination
- -Minimum interval between each of the doses is 4 weeks
-  Given at 9 and 18 months of age or first contact after this age
-  Can also be given to any unimmunised child of 6-9 months
-  old who has been exposed to measles patients. Children vaccinated in this way must have the vaccination repeated at 9 months of age
- ~ Vaccination of sick children
-  Admit and treat any child who is severely ill, and vaccinate at the time of discharge
-  Minor illness is not a contraindication to vaccination
-  Screen clients at points of care and administer the due vaccines
-  Screen clients for vaccine preventable diseases for investigation and notification
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 18.1.1 General principles of routine childhood immunization match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 18.1 ROUTINE CHILDHOOD VACCINATION > 18.1.2 Hepatitis B Vaccination

### 195. narrative-2107
**Pages:** ? | **Section:** 18.1.2 Hepatitis B Vaccination
**Validation:** No validation data | **Condition:** Hepatitis

**Audit hash:** `3f46393afd94ee71...`

#### Extracted Content
```
- ~ Since 2005, children are immunised against Hepatitis B in the routine childhood immunization using the DPT-HepBHib vaccine at 6, 10, and 14 weeks of age

Uganda Clinical Guidelines 2023

CHAPTER 18: Immunization

881

Uganda Clinical Guidelines 2023

CHAPTER 18: Immunization

882

- ~ For adolescents and adults, it is recommended that the hepatitis B vaccination is given preferably after testing for hepatitis B infection (HBsAg and Anti-HBs). Patients with HIV and pregnant women should be handled on a case by case basis
- ~ Vaccination is recommended for high risk groups, e.g:
- -Health workers in clinical settings and training
- -Persons who frequently receive blood transfusions
- Intravenous drugs users
- Recipients of solid organ transplantation
- Partners and household contacts of HBsAg positive patients
- -High-risk sexual behaviour
- -Support staff in health facilities
- ~ The schedule has three doses: at 0, 1 month after 1st dose, and 6 months after first dose (0, 1, 6 months)
- ~ The storage temperature for the vaccine is 2°C to 8°C
-  Dose: 0.5 mL given intramuscularly on the deltoid muscle (upper arm)
-  Do NOT give vaccine on the buttocks because of low immune response (decreased protective antibody response) and risks of injury to the sciatic nerve
```

#### Extracted Clinical Flags
- **Special populations:** pregnant women should be handled on a case by case basis
- ~ Vaccination is recommended for high ris

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Special populations: pregnant women should be handled on a case by case basis
- ~ Vaccination is recommended for high ris.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 18.1.2 Hepatitis B Vaccination match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 19.1 NUTRITION GUIDELINES IN SPECIAL POPULATIONS > 19.1.1 Infant and Young Child Feeding (IYCF)

### 196. narrative-2117
**Pages:** ? | **Section:** 19.1.1 Infant and Young Child Feeding (IYCF)
**Validation:** No validation data

**Audit hash:** `0414c074a3746036...`

#### Extracted Content
```
- 1. Counsel and support all mothers to initiate breastfeeding within an hour of delivery and exclusively breastfeed their infants for the first six months of life, unless medically contraindicated.
- 2. Teach mother correct positioning and attachment for breastfeeding, how to express and store breast milk hygienically, and how to feed the child by a cup.
- 3. Counsel and support parents to introduce adequate, safe, and appropriate complementary foods at 6 months of age, and to continue breast feeding until the child is 2 years.
- 4. A good diet should be adequate in quantity and include an energy-rich food (e.g. thick cereal with added oil, meat, fish, eggs, legumes, fruits and vegetables)
- 5. Pregnant women and lactating mothers should consume adequate nutritious foods
- 6. Recommend exclusive breastfeeding for infants of HIV-infected women for the first 6 months unless the replacement is acceptable, feasible, affordable, sustainable, and safe (AFASS).
- 7. Malnourished children should be provided with appropriate medical care, nutritional rehabilitation, and follow-up.
- 8. Encourage mothers of low birth weight infants who can suckle to breastfeed. Assist those who cannot breastfeed to express breast milk and feed the baby.
- 9. During illness, children should take increased fluids: breastfeed more often, increase amount of milk given, increase fluid intake (e.g. soups, yoghurt, and drinking water). Extra fluid in diarrhoea is especially life-saving
- 10. For more information on feeding recommendations in infants and young children, see IMCI section 17.3.12.3

Uganda Clinical Guidelines 2023

CHAPTER 19: Nutrition

887

Uganda Clinical Guidelines 2023

CHAPTER 19: Nutrition

888
```

#### Extracted Clinical Flags
- **Special populations:** Pregnant women and lactating mothers should consume adequate nutritious foods
- 6

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Special populations: Pregnant women and lactating mothers should consume adequate nutritious foods
- 6.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.1.1 Infant and Young Child Feeding (IYCF) match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 19.1 NUTRITION GUIDELINES IN SPECIAL POPULATIONS > 19.1.3 Nutrition in Diabetes

### 197. narrative-2121
**Pages:** ? | **Section:** 19.1.3 Healthy eating and exercise in diabetics help to:
**Validation:** No validation data | **Condition:** Diabetes

**Audit hash:** `cd246a82802827d0...`

#### Extracted Content
```
-  Maintain the blood glucose close to normal to prevent complications
-  Control cholesterol levels
-  Control blood pressure, and reduce the risk of complications such as heart disease and stroke

In addition, diabetics have to take care to balance their food with insulin and oral antidiabetic medications to help manage their blood glucose levels.

Healthy diet involves eating a variety of foods including vegetables, whole grains, fruits, non-fat dairy products, beans, lean meat, poultry, and fish. These are rich in vitamins, minerals and fibre. Avoid processed foods.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.1.3 Healthy eating and exercise in diabetics help to: match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 198. narrative-2122
**Pages:** ? | **Section:** 19.1.3 General advice
**Validation:** No validation data | **Condition:** Diabetes

**Audit hash:** `ea1ce376cb8db919...`

#### Extracted Content
```
- ~ Eat three meals a day. Avoid skipping meals, and space out breakfast, lunch, and evening meal over the day
- ~ At each meal, include moderate amount (around 1/3 of the plate) of starchy carbohydrate foods, e.g., bread, pasta, chapatis, potatoes, yams, noodles, rice, and cereals. Eat more slowly absorbed (low glycaemic index) foods, e.g., pasta, rice, sweet potato and yam, porridge oats, bran, and natural muesli
- ~ Reduce fat in the diet, especially saturated fats. Use unsaturated fats or oils e.g. olive oil, sunflower oil
- ~ Eat more fruit and vegetables. Aim for at least five portions a day. Eat more beans and lentils.
- ~ Limit sugar and sugary foods
- ~ Reduce salt in the diet to 6 g or less per day
- ~ Drink alcohol only in moderation: 1 drink (one beer or one small glass of wine or one shot of spirit) for women and

Uganda Clinical Guidelines 2023

CHAPTER 19: Nutrition

889

Uganda Clinical Guidelines 2023

CHAPTER 19: Nutrition

890

2 for men as a maximum amount daily. Alcohol has some cardioprotective effect. It should be consumed with food to prevent hypoglycaemia

- ~ Don't use products marketed as "diabetic foods, drinks or herbs" (they are expensive and of no benefit)
- ~ Routine supplementation with vitamins and minerals without underlying actual deficiency is not beneficial, patients should eat lots of fruits and vegetables e.g, a combination of selenium and molinga has been proven to be beneficial
- ~ Obese and overweight patients need to be encouraged to reduce weight using exercise and diet modifications
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.1.3 General advice match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 19.2 MALNUTRITION ICD10 CODE: E40-43 > 19.2.1 Introduction on Malnutrition

### 199. narrative-2124
**Pages:** ? | **Section:** 19.2.1 Note
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `95cfc49fb735e993...`

#### Extracted Content
```
-  Previously, malnutrition was classified into two types: 1) ProteinEnergy Malnutrition (PEM) due to lack of adequate protein and energy in the diet and 2) Micronutrient malnutrition-due to deficiencies in specific micronutrients (vitamins and minerals).
-  These causal names are now avoided because protein and energy deficits are likely to be accompanied by deficiencies of other nutrients, and management of malnutrition takes this into consideration.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.2.1 Note match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 19.2 MALNUTRITION ICD10 CODE: E40-43 > 19.2.1 Introduction on Malnutrition > 19.2.1.2 Assessing Malnutrition in Children 6 months to 5 years

### 200. narrative-2130
**Pages:** ? | **Section:** 19.2.1.2 Investigations
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `86773ce7cdfdd39f...`

#### Extracted Content
```
Children with SAM should always be first assessed with a full clinical examination to confirm presence of any danger sign, medical complications, and tested for appetite.

-  Assess patient's history of:
-  Recent intake of food, loss of appetite, breastfeeding
-  Usual diet before current illness (compare the answers to the Feeding Recommendations for the Child's age (section 17.3.12.3)
-  Duration, frequency and type of diarrhoea and vomiting
-  Family circumstances
-  Cough &gt;2 weeks and contact with TB
-  Contact with measles
-  Known or suspected HIV infection/exposure
-  Initial examination for danger signs and medical complications:
-  Shock: lethargy or unconscious, cold hands, slow capillary refill (&lt;3 seconds), weak pulse, low blood pressure
-  Signs of dehydration
-  Severe palmar pallor
-  Bilateral pitting oedema
-  Eye signs of vitamin A deficiency: dry conjunctiva, corneal ulceration, keratomalacia, photophobia
-  Local signs of infection: ear, throat, skin, pneumonia
-  Signs of HIV (see WHO Clinical Staging section 3.1.1)
-  Fever (³37.5°C) or hypothermia (rectal temp &lt;35.5°C)
-  Mouth ulcers
-  Skin changes of kwashiorkor: hypo- or hyperpigmentation, desquamation, ulcerations all over the body, exudative lesions (resembling burns) with secondary infection (including candida)

Uganda Clinical Guidelines 2023

CHAPTER 19: Nutrition

895

Uganda Clinical Guidelines 2023

CHAPTER 19: Nutrition

896

-  Laboratory tests
-  Blood glucose
- -Complete blood count or Hb, malaria, HIV, electrolytes
- -Stool microscopy for ova and cysts, occult blood, and parasites
-  Chest X-ray: Look for evidence of tuberculosis or other chest abnormalities
-  Conduct an appetite test
- -Assess all children ³6 months for appetite at the initial visit and at every follow up visit to the health facility
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 19.2.1.2 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 19.2 MALNUTRITION ICD10 CODE: E40-43 > 19.2.2 Management of Acute Malnutrition in Children

### 201. narrative-2134
**Pages:** ? | **Section:** 19.2.2 General principles of management
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `a385620e94fc1d0d...`

#### Extracted Content
```
- ~ Admit all children with any danger sign, medical complications, pitting oedema or those who fail appetite tests for inpatient care and treatment for complicated SAM.
-  Keep them in a warm area separated from infectious children, or in a special nutrition area.
- ~ Children with good appetite and no medical complications can be managed as outpatients for uncomplicated SAM.
- ~ Adequate facilities and staff to ensure correct preparation of therapeutic foods, and to feed child regularly day and night, should be available.
- ~ Accurate weighing machines and MUAC tapes should be available
- ~ Proper records of feeds given and child's measurements should be kept so that progress can be monitored
- ~ Explain to patient/care-giver to handle the child gently
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2 General principles of management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 19.2 MALNUTRITION ICD10 CODE: E40-43 > 19.2.2 Management of Acute Malnutrition in Children > 19.2.2.3 Management of Complicated Severe Acute Malnutrition

### 202. narrative-2140
**Pages:** ? | **Section:** 19.2.2.3 Note
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `675eab968ef16164...`

#### Extracted Content
```
-  Iron is given after 2 days on F-100; if patient is taking RUTF, do NOT give iron
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.3 Note match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 203. narrative-2148
**Pages:** ? | **Section:** 19.2.2.3 TREATMENT
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `3a61ec8a0b65c289...`

#### Extracted Content
```
-  Keep the ward closed during the night and avoid wind drafts inside
-  Give appropriate IV or IM antibiotics
-  Change wet nappies, clothes and bedding to keep child and bed dry
-  Quickly clean the patient with a warm wet towel and dry immediately. Avoid washing the baby directly in the first few weeks of admission
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.3 TREATMENT match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 204. narrative-2150
**Pages:** ? | **Section:** 19.2.2.3 Dehydration
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `17e35d4a5ebbfa34...`

#### Extracted Content
```
- ~ In both oedema and non-oedematous SAM, the margin of safety between dehydration and over-hydration is very narrow. Exercise care and caution to avoid over-hydration and risk of cardiac failure
-  Assume that all children with watery diarrhoea or reduced urine output have some dehydration
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.3 Dehydration match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 205. narrative-2155
**Pages:** ? | **Section:** 19.2.2.3 Monitoring
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `202989da497c1195...`

#### Extracted Content
```
- ~ ONLY rehydrate until the weight deficit is corrected and then STOP, DO NOT give extra fluid to "prevent recurrence" (from specialist's notes)
- ~ During rehydration, respiration and pulse rate should fall and urine passing should start
- ~ Return of tears, moist mouth, improved skin tugor and less sunken eyes and fontanelle are a sign of rehydration. SAM children will not show these and so weight gain should be measured
- ~ Monitor progress of rehydration every 30 minutes for 2 hours, then every hour for the next 4-10 hours
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.3 Monitoring match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 206. narrative-2161
**Pages:** ? | **Section:** 19.2.2.3 Broad spectrum antibiotics
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `d1811ae3d2237efc...`

#### Extracted Content
```
-  Benzylpenicillin 50,000 IU/kg IM or IV every 6 hours Or ampicillin 50 mg/kg every 6 hours for 2 days f Then, oral amoxicillin 25-40 mg/kg every 8 hours for

- [ ]  5 days PLUS

-  Gentamicin 7.5 mg/kg once a day for 7 days
-  Measles vaccination

- [ ]  If child is ³ 6 months and not vaccinated, or was vaccinated before 9 months of age. Delay vaccination if child is in shock
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.3 Broad spectrum antibiotics match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 207. narrative-2164
**Pages:** ? | **Section:** 19.2.2.3 Micronutrient deficiencies
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `00d053d6f0a08a34...`

#### Extracted Content
```
- ~ All SAM children have vitamin and mineral deficiencies
- ~ Anaemia is common, but DO NOT give iron initially, instead wait until the child has a good appetite and has started gaining weight, usually in the second week, because iron can make infections worse
- ~ RUTF already contains adequate iron so do not add. F-100 does not contain iron, so iron supplements are needed

Uganda Clinical Guidelines 2023

CHAPTER 19: Nutrition

905

Uganda Clinical Guidelines 2023

CHAPTER 19: Nutrition

906

- ~ F-75, F-100 and RUTF already contain multivitamins (including vitamin A and folic acid) zinc and copper. Additional doses are not needed
- ~ If there are no eye signs or history of measles, then do not give a high dose of vitamin A as therapeutic foods already contain adequate amounts
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.3 Micronutrient deficiencies match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 208. narrative-2166
**Pages:** ? | **Section:** 19.2.2.3 Iron
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `46f11e49db0ec86e...`

#### Extracted Content
```
-  Give iron in the second week of nutritional rehabilitation
- -Do not give in the stabilization phase
- Do not give in children receiving RUTF
-  Start iron at 3 mg/kg per day after 2 days on F-100 catch- up formula

If child is not on any pre-mixed therapeutic foods, give the following micronutrients daily for at least 2 weeks

-  Folic acid at 5 mg on day 1; then 1 mg daily Multivitamin syrup 5 ml
-  Zinc 2 mg/kg per day
-  Copper at 0.3 mg/kg per day
-  Other vitamins and minerals e.g, a combination of selenium and moringa has been proven to be beneficial
```

#### Extracted Clinical Flags
- **Contraindications:** the stabilization phase
- Do not give in children receiving RUTF
-  Start iron at 3 mg/kg per day after 2 days on F-100 catch- up formula

If child is not on any pre-mixed therapeutic foods, give the following micronutrients daily for at least 2 weeks

-  Folic acid at 5 mg on day 1

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: the stabilization phase
- Do not give in children receiving RUTF
-  Start iron at 3 mg/kg per day after 2 days on F-100 catch- up formula

If child is not on any pre-mixed therapeutic foods, give the following micronutrients daily for at least 2 weeks

-  Folic acid at 5 mg on day 1.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.3 Iron match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 19.2 MALNUTRITION ICD10 CODE: E40-43 > 19.2.2 Management of Acute Malnutrition in Children > 19.2.2.4 Treatment of Associated Conditions

### 209. narrative-2197
**Pages:** ? | **Section:** 19.2.2.4 TREATMENT
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `9b7932b213963e6d...`

#### Extracted Content
```
Avoid using nappies so that the perinuem can stay dry
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.4 TREATMENT match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 210. narrative-2199
**Pages:** ? | **Section:** 19.2.2.4 If child has signs of heart failure
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `dc6c9e11fbd2920d...`

#### Extracted Content
```
- Furosemide, 1 mg/kg at the start of the transfusion
-  Give 10 mL/kg of packed cells, as whole blood may worsen heart failure
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.4 If child has signs of heart failure match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 211. narrative-2201
**Pages:** ? | **Section:** 19.2.2.4 Monitoring
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `998b3f15f1e3b97a...`

#### Extracted Content
```
- ~ Monitor pulse and breathing rates, listen to lung fields, examine adbomen for liver size, check jugular venous pressure every 15 minutes during transfusion
- -If either breathing rate increases by 5 breaths/minute or heart rate increases by 25 beats/minute, transfuse more slowly
- -If there are basal lung crepitations or an enlarging liver, stop transfusion and give IV furosemide IV at 1 mg/kg

Apply barrier cream (zinc and castor oil ointment or petroleum jelly) to the raw areas, and gentian violet or nystatin cream to skin sores

Uganda Clinical Guidelines 2023

CHAPTER 19: Nutrition

915

Uganda Clinical Guidelines 2023

CHAPTER 19: Nutrition

916
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.4 Monitoring match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 212. narrative-2202
**Pages:** ? | **Section:** 19.2.2.4 TREATMENT
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `7bd84cb436b72510...`

#### Extracted Content
```
If Giardiasis suspected or confirmed by stool microscopy



Give metronidazole 7.5 mg/kg every 8 hours for 7 days
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.4 TREATMENT match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 19.2 MALNUTRITION ICD10 CODE: E40-43 > 19.2.2 Management of Acute Malnutrition in Children > 19.2.2.5 Discharge from Nutritional Programme

### 213. narrative-2207
**Pages:** ? | **Section:** 19.2.2.5 Discharge from Nutritional Programme
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `3b637f32454515b4...`

#### Extracted Content
```
Percentage weight gain should not be used as a criterion

Feeding after discharge from nutritional programme Counsel the mother on feeding and other issues as in the table below

Use a cereal-based starter F-75, or if necessary, a commercially available isotonic starter
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.5 Discharge from Nutritional Programme match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 214. narrative-2209
**Pages:** ? | **Section:** 19.2.2.5 Additional instructions
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `a6b34332056e6663...`

#### Extracted Content
```
- ~ How to continue any needed medications at home
- ~ Danger signs to bring child back for immediate care
- ~ When and where to go for planned follow-up: at 1 week, 2 weeks, 1 month, 3 months, and 6 months; then twice a year until when the child is 3 years old
- ~ Where and when to take child for growth monitoring and promotion on monthly basis up to 2 years
- ~ When to return for next immunisation, vitamin A, and deworing
- ~ How to continue stimulating the child at home with play acti ities
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 19.2.2.5 Additional instructions match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 19.2 MALNUTRITION ICD10 CODE: E40-43 > 19.2.3 SAM in Infants Less than 6 Months

### 215. narrative-2211
**Pages:** ? | **Section:** 19.2.3 SAM in Infants Less than 6 Months
**Validation:** No validation data | **Condition:** Malnutrition

**Audit hash:** `074ead013787a816...`

#### Extracted Content
```
SAM in infants &lt;6 months is rare. An organic cause or failure to thrive should be considered and treated. Admit the infant with SAM if any of the following are present:

- ~ General danger signs or serious condition
- ~ Recent weight loss or failure to gain weight
- ~ Ineffective breastfeeding (attachment, positioning, or suckling) directly observed for 15-20 minutes
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 19.2.3 SAM in Infants Less than 6 Months match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 20.1 INFECTIONS AND INFLAMMATORY EYE CONDITIONS > 20.1.2 Conjunctivitis ("Red Eye")

### 216. narrative-2229
**Pages:** ? | **Section:** 20.1.2 Investigations
**Validation:** No validation data

**Audit hash:** `2dbdb895f5527227...`

#### Extracted Content
```
-  Clinical features are diagnostic
-  Pus swab for culture and sensitivity
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 20.1.2 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 217. narrative-2232
**Pages:** ? | **Section:** 20.1.2 Prevention
**Validation:** No validation data

**Audit hash:** `e4f97970cd6a5e46...`

#### Extracted Content
```
- ~ Personal hygiene; daily face washing
- ~ Avoid irritants and allergens

~
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 20.1.2 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 20.2 DECREASED OR REDUCED VISION CONDITIONS > 20.2.1.1 Paediatric Cataract ICD10 CODE: H26.0

### 218. narrative-2275
**Pages:** ? | **Section:** 20.2.1.1 Investigations
**Validation:** No validation data

**Audit hash:** `7160675763d7d908...`

#### Extracted Content
```
-  If at HC2 or HC3, reassure patient and refer to hospital
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify Level of Care assignments (HC2, HC3, HOSPITAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 20.2.1.1 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 20.2 DECREASED OR REDUCED VISION CONDITIONS > 20.2.2 Glaucoma

### 219. narrative-2281
**Pages:** ? | **Section:** 20.2.2 Management
**Validation:** No validation data

**Audit hash:** `94c1a18702d171b8...`

#### Extracted Content
```
- ~ Goal of treatment is to arrest/delay progress of the disease, not for visual improvement. Therapy is usually life long
- ~ Angle-closure glaucoma is a medical emergency that requires urgent reduction of intra ocular pressure
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 20.2.2 Management match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 21.1 EAR CONDITIONS > 21.1.6 Mastoiditis

### 220. narrative-2335
**Pages:** ? | **Section:** 21.1.6 Investigations
**Validation:** No validation data

**Audit hash:** `b62efe39db6d2776...`

#### Extracted Content
```
-  Diagnosis mainly by clinical features
-  X-ray: Useful in chronic mastoiditis
-  Blood: Full blood count, shows leucocytosis
-  Examine ear with otoscope
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 21.1.6 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 21.2 NASAL CONDITIONS > 21.2.2 Epistaxis (Nose Bleeding)

### 221. narrative-2347
**Pages:** ? | **Section:** 21.2.2 Prevention
**Validation:** No validation data

**Audit hash:** `878274c5d6433fb5...`

#### Extracted Content
```
- ~ Avoid picking the nose
- ~ Treat/control predisposing conditions
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 21.2.2 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 21.3 THROAT CONDITIONS > 21.3.1 Foreign Body (FB) in the Airway ICD10 CODE: T17

### 222. narrative-2376
**Pages:** ? | **Section:** 21.3.1 Prevention
**Validation:** No validation data

**Audit hash:** `3fceec8e60d9360f...`

#### Extracted Content
```
- ~ Do not give groundnuts or other small hard food items to children &lt;2 years
- ~ If a child is found with objects in the mouth, leave the child alone to chew and swallow or gently persuade the child to spit out the object
-  Do not struggle with/force the child
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 21.3.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 21.3 THROAT CONDITIONS > 21.3.2 Foreign Body in the Food Passage ICD10 CODE: T18

### 223. narrative-2382
**Pages:** ? | **Section:** 21.3.2 Prevention
**Validation:** No validation data

**Audit hash:** `7cf822f03a0d52b0...`

#### Extracted Content
```
- ~ Keep potential FBs out of children's reach
- ~ Advise on care in eating, i.e., not taking in too large pieces of food, chewing thoroughly before swallowing
- ~ Advise once a FB is stuck to avoid trying to "push" it down with solid food as this may sometimes be fatal
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 21.3.2 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 22.2 VIRAL SKIN INFECTIONS > 22.2.1 Herpes Simplex

### 224. narrative-2424
**Pages:** ? | **Section:** 22.2.1 Prevention
**Validation:** No validation data | **Condition:** Skin conditions

**Audit hash:** `8c22dd4096aa94a6...`

#### Extracted Content
```
Provide health education on

- ~ Personal hygiene
- ~ Avoiding direct contact with infected people
- ~ Use of gloves and condoms as applicable
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 22.2.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 22.3 FUNGAL SKIN INFECTIONS > 22.3.1 Tineas

### 225. narrative-2438
**Pages:** ? | **Section:** 22.3.1 Prevention and health education
**Validation:** No validation data | **Condition:** Skin conditions

**Audit hash:** `afd275015851b7d2...`

#### Extracted Content
```
- ~ Clean all contaminated objects, e.g., combs, brushes
- ~ Avoid sharing contaminated combs, towels, clothes, etc.
- ~ Advise patient on the need to persist with the long durations of treatment to completely clear infection
- ~ Personal foot hygiene is important. Keep feet clean and dry. Wash socks daily
- ~ If patient has repeat fungal infections, refer him/her for HIV, diabetes counselling and testing.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 22.3.1 Prevention and health education match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 22.4 PARASITIC SKIN INFECTIONS

### 226. narrative-2444
**Pages:** ? | **Section:** 22.4 Prevention
**Validation:** No validation data | **Condition:** Skin conditions

**Audit hash:** `bd307b33913aaf41...`

#### Extracted Content
```
- ~ Personal hygiene (washing clothes and regular bathing)
- ~ Avoid close contact with infected people
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 22.4 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 22.4 PARASITIC SKIN INFECTIONS > 22.4.2 Pediculosis/Lice

### 227. narrative-2450
**Pages:** ? | **Section:** 22.4.2 Prevention
**Validation:** No validation data | **Condition:** Skin conditions

**Audit hash:** `3a16a3aeeda9dafe...`

#### Extracted Content
```
- ~ Personal hygiene (washing clothes and regular bathing)
- ~ Avoid close contact with infected people
- ~ Treat the whole family
- ~ Avoid sharing combs, towels, etc
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 22.4.2 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 22.4 PARASITIC SKIN INFECTIONS > 22.4.3 Tungiasis (Jiggers)

### 228. narrative-2457
**Pages:** ? | **Section:** 22.4.3 Investigations
**Validation:** No validation data | **Condition:** Skin conditions

**Audit hash:** `2d8f66bf32a8ad91...`

#### Extracted Content
```
- ~ Clinical features are diagnostic
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 22.4.3 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 22.5 INFLAMMATORY AND ALLERGIC SKIN CONDITIONS

### 229. narrative-2465
**Pages:** ? | **Section:** 22.5 Investigations
**Validation:** No validation data | **Condition:** Skin conditions

**Audit hash:** `ab59d031ce1ab023...`

#### Extracted Content
```
-  Clinical features are largely diagnostic
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 22.5 Investigations match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 22.5 INFLAMMATORY AND ALLERGIC SKIN CONDITIONS > 22.5.2 Urticaria/Papular Urticari

### 230. narrative-2472
**Pages:** ? | **Section:** 22.5.2 Prevention
**Validation:** No validation data | **Condition:** Skin conditions

**Audit hash:** `e290b3227672a8d6...`

#### Extracted Content
```
- ~ Avoid contact with known allergens
- ~ Treat helminth infections
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 22.5.2 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 22.5 INFLAMMATORY AND ALLERGIC SKIN CONDITIONS > 22.5.3 Eczema (Dermatitis)

### 231. narrative-2477
**Pages:** ? | **Section:** 22.5.3 Prevention
**Validation:** No validation data | **Condition:** Skin conditions

**Audit hash:** `3a79564c27435b90...`

#### Extracted Content
```
- ~ Avoid contact with allergens, Advise on light dressing in hot weather to avoid sweating, advise on bathing habits like; reduce on frequency of bathing - at most twice daily, use soft sponge.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 22.5.3 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 22.6 SKIN ULCERS AND CHRONIC WOUNDS > 22.6.1 Leg Ulcers

### 232. narrative-2487
**Pages:** ? | **Section:** 22.6.1 Prevention
**Validation:** No validation data | **Condition:** Skin conditions

**Audit hash:** `8749d2691f91c3a9...`

#### Extracted Content
```
- ~ Ensure personal hygiene
- ~ Ensure good nutrition
- ~ Avoid trauma
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 22.6.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 22.7 DRUG-INDUCED SKIN REACTIONS > 22.7.1 Steven-Johnson Syndrome (SJS) and Toxic Epidermal Necrolysis (TEN) ICD10 CODE: L51

### 233. narrative-2493
**Pages:** ? | **Section:** 22.7.1 Prevention
**Validation:** No validation data | **Condition:** Skin conditions

**Audit hash:** `a0244303262d22e2...`

#### Extracted Content
```
- ~ Take thorough medicine history
- ~ Advise patients to avoid self-medication
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 22.7.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 23.2 ORO-DENTAL INFECTIONS > 23.2.2 Dental Caries > 23.2.2.1 Nursing Caries

### 234. narrative-2523
**Pages:** ? | **Section:** 23.2.2.1 Prevention
**Validation:** No validation data | **Condition:** Oral health

**Audit hash:** `0e4d37475f52c44c...`

#### Extracted Content
```
-  Educate care taker to avoid frequent on-demand liquids at night including breastfeeding, after 15 months
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 23.2.2.1 Prevention match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 24.1 SURGERY > 24.1.2 Internal Haemorrhage

### 235. narrative-2605
**Pages:** ? | **Section:** 24.1.2 Internal Haemorrhage
**Validation:** No validation data

**Audit hash:** `95c56aaf3c3292c0...`

#### Extracted Content
```
Internal bleeding (also called internal haemorrhage) is a loss of blood that occurs from the vascular system into a body cavity or space. It is

Uganda Clinical Guidelines 2023

CHAPTER 24 : Surgery, Radiology and Anaesthesia

1041

Uganda Clinical Guidelines 2023

CHAPTER 24 : Surgery, Radiology and Anaesthesia

1042

a serious medical emergency and the extent of severity depends on:
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 24.1.2 Internal Haemorrhage match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 236. narrative-2607
**Pages:** ? | **Section:** 24.1.2 Internal Haemorrhage
**Validation:** No validation data

**Audit hash:** `a15c3ab579383559...`

#### Extracted Content
```
Location of the bleeding (damage to organs, even with relatively limited amounts: see specific chapters)

Severe bleeding in a body cavity/space is an emergency condition with unstable vital signs (e.g., ruptured spleen, ruptured tubal pregnancy)
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 24.1.2 Internal Haemorrhage match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 24.1 SURGERY > 24.1.4 Newborn with Surgical Emergencies

### 237. narrative-2612
**Pages:** ? | **Section:** 24.1.4 Newborn with Surgical Emergencies
**Validation:** No validation data | **Condition:** Neonatal care

**Audit hash:** `55c7e9d6bc99bbf7...`

#### Extracted Content
```
Babies may be born at lower health facilities with congenital defects that require emergency surgical intervention at tertiary levels:

- -The common surgical emergencies in neonates include: gastroschisis (defect of abdominal wall with intestine sticking outside the body), tracheoesophageal fistula, imperforate anus, and spina bifida
- -If diagnosed in lower level health facilities (HCII, HCIII, HCIV, District Hospital), apply general principles of supportive management of the newborn
-  The aim should be to avoid hypothermia, inimize risk of infection, ensure adequate hydration, and inimize risk of aspiration and hypoglycaemia
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- [ ] **Conditional Logic** — Verify Level of Care assignments (DISTRICTHOSPITAL) match the source PDF. Confirm referral pathways between facility levels are intact.
- [ ] **Provenance** — Confirm source page unknown and section 24.1.4 Newborn with Surgical Emergencies match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 24.1 SURGERY > 24.1.5 Surgical Antibiotic Prophylaxis

### 238. narrative-2615
**Pages:** ? | **Section:** 24.1.5 General principles
**Validation:** No validation data

**Audit hash:** `2dae50c809cfbe6b...`

#### Extracted Content
```
- ~ The need of prophylaxis depends on the nature of the expected wound
- -Wounds that are expected to be clean (no inflammation,
- -And respiratory, genital, urinary and alimentary tract not entered) generally DO NOT require prophylaxis except where the consequences of surgical site infection could be severe (e.g., joint replacements)
- -Prophylaxis is indicated in cases of clean-contaminated wounds (entering respiratory, genital, urinary and alimentary tracts but no unusual contamination)
- -Treatment with a course of antibiotics is indicated in
- -procedures with contaminated wounds (fresh open accidental wounds, operations with major breaks in sterile techniques), dirty or infected wounds (old traumatic wounds with retained necrotic tissue, clinical infection, perforated viscera)
- ~ Prophylaxis is given &lt;60 minutes before the first incision
- ~ Refer to institution-specific protocols for details

Prophylaxis is not recommended for most uncomplicated clean procedures

One single dose prior to the procedure is usually sufficient

Routine post-operative antimicrobial administration is NOT recommended for most surgeries as it causes wastage of limited resources, causes unnecessary side effects to the patient and can lead to antimicrobial resistance.
```

#### Extracted Clinical Flags
- **Contraindications:** most uncomplicated clean procedures

One single dose prior to the procedure is usually sufficient

Routine post-operative antimicrobial administration is NOT recommended for most surgeries as it causes wastage of limited resources, causes unnecessary side effects to the patient and can lead to antimicrobial resistance

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria. Extracted contraindications: most uncomplicated clean procedures

One single dose prior to the procedure is usually sufficient

Routine post-operative antimicrobial administration is NOT recommended for most surgeries as it causes wastage of limited resources, causes unnecessary side effects to the patient and can lead to antimicrobial resistance.
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 24.1.5 General principles match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 24.2 DIAGNOSTIC IMAGING > 24.2.1 Diagnostic Imaging: A Clinical Perspective

### 239. narrative-2618
**Pages:** ? | **Section:** 24.2.1 Basic Diagnostic Imaging Modalities
**Validation:** No validation data

**Audit hash:** `86cc6952b95168e0...`

#### Extracted Content
```
-  Plain Radiography (Hospital)
-  Ultrasound scan (HC4 and Hospital)
- -Ultrasound is non-invasive and does not use ionising radiation. Therefore, when indicated, it is the most appropriate imaging modality for children and pregnant women.
```

#### Extracted Clinical Flags
- **Special populations:** pregnant women

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 24.2.1 Basic Diagnostic Imaging Modalities match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 24.3 ANAESTHESIA > 24.3.3 Selection of Type of Anaesthesia for the Patient > 24.3.3.1 Techniques of General Anaesthesia

### 240. narrative-2643
**Pages:** ? | **Section:** 24.3.3.1 RAPID SEQUENCE INDUCTION OF GENERAL ANAESTHESIA
**Validation:** No validation data

**Audit hash:** `69be9e8ccab36ec4...`

#### Extracted Content
```
- -Monitor vital signs (as above)
- ~ At the end of the operation when the patient shows signs of respiratory effort, give
- -IV. Neostigmine 0.03 to 0.07 mg/kg to reverse the
- -effects of the long acting muscle relaxant
```

#### Verification Checklist
- [ ] **Dosage Accuracy** — Verify any dose values mentioned match source PDF page unknown.
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 24.3.3.1 RAPID SEQUENCE INDUCTION OF GENERAL ANAESTHESIA match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 241. narrative-2644
**Pages:** ? | **Section:** 24.3.3.1 Indication
**Validation:** No validation data

**Audit hash:** `e1ccd9143dbd3c0c...`

#### Extracted Content
```
- ~ All operations that require a protected airway and controlled ventilation, e.g, intraabdominal, intrathoracic, and intracranial operations

(Also called crash induction) For patients with "full stomach" and at risk of regurgitation, e.g., emergency surgery, distended abdomen
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 24.3.3.1 Indication match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### Section: 24.3 ANAESTHESIA > 24.3.3 Selection of Type of Anaesthesia for the Patient > 24.1.1.1 Techniques for Regional Anaesthesia

### 242. narrative-2647
**Pages:** ? | **Section:** 24.1.1.1 PROCEDURE
**Validation:** No validation data

**Audit hash:** `f23329279e708286...`

#### Extracted Content
```
- ~ Discuss the procedure with the patient
- ~ Identify the injection site using appropriate landmarks
- ~ Observe aseptic conditions
- ~ Use small bore needle, which causes less pain during injection
- ~ Select concentration and volume of drug according to the technique
- ~ Aspirate before injection to avoid accidental intravascular injection
- ~ Inject slowly and allow 5-10 minutes for onset of drug action
- ~ Confirm desired block effect before surgery commences
- ~ The patient must be monitored throughout the procedure
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 24.1.1.1 PROCEDURE match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 243. narrative-2659
**Pages:** ? | **Section:** 24.1.1.1 Other PPE
**Validation:** No validation data

**Audit hash:** `61b3d8be46e18fc0...`

#### Extracted Content
```
- ~ Wear a surgical or procedure mask and eye protection (googles or glasses) or a face shield when performing activities which are likely to generate splashes or sprays of blood, body fluids, secretions or excretions
- ~ Wear a gown to protect skin and prevent soiling of clothing in activities as above
- ~ Use a waterproof bandage to cover wounds
- ~ Wear protective boots and gloves and where possible, wear a water-proof apron when working in a heavily contaminated area, e.g., toilets
- ~ Avoid mouth-to-mouth resuscitation and pipetting by mouth where possible
- ~ In surgical procedures, use a needle holder and appropriate sized needle, wear double gloves and eye shield
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 24.1.1.1 Other PPE match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 244. narrative-2660
**Pages:** ? | **Section:** 24.1.1.1 Safe handling of sharps
**Validation:** No validation data

**Audit hash:** `7f7b468da535b19e...`

#### Extracted Content
```
- ~ Ensure safe sharps handling and disposal
- ~ Avoid accidental pricks and cuts with contaminated sharp instruments (e.g., needles) by careful handling and proper disposal
- ~ Use "hands-free" technique for passing sharp instruments
- ~ Keep a puncture-resistant container nearby
- ~ Use safe injection practices:
- -Use a sterile needle and syringe for every injection
- -Do not recap, bend, or break needles after use
- ~ Drop all used disposable needles, plastic syringes, and blades directly into the sharps container without recapping or passing to another person
- ~ Empty or send for incineration when container is full
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- ~~**Stratification**~~ — Not applicable
- [ ] **Contraindications** — Check for warnings, danger signs, and referral criteria.
- ~~**Conditional Logic**~~ — Not applicable
- [ ] **Provenance** — Confirm source page unknown and section 24.1.1.1 Safe handling of sharps match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

### 245. narrative-2678
**Pages:** ? | **Section:** 24.1.1.1 National Laboratory Test Menu
**Validation:** No validation data

**Audit hash:** `57e56509386da469...`

#### Extracted Content
```
The test menu was developed by Ministry of Health/Uganda National Health Laboratory Services (UNHLS). It is a list of tests that are available at the specified level of health care. The laboratory system of Uganda is designed to support the minimum health care package for each level of care, with complexity of tests increasing with the level of care.

The laboratory test menu has been included in UCG 2023, in order to guide clinicians about the laboratory services available at each level of health care, and where to refer a patient in need of a particular test.
```

#### Verification Checklist
- ~~**Dosage Accuracy**~~ — Not applicable
- [ ] **Stratification** — Confirm any age/weight stratifications mentioned are correctly preserved.
- ~~**Contraindications**~~ — Not applicable
- [ ] **Conditional Logic** — Verify any IF/THEN logic, referral criteria, or decision pathways are intact.
- [ ] **Provenance** — Confirm source page unknown and section 24.1.1.1 National Laboratory Test Menu match the printed WHO guidelines.

**Decision:** ☐ Approved  ☐ Flagged  ☐ Corrected

**Reviewer notes:** _____

**Corrections (if any):** _____

---

---

## Appendix: Reviewer Sign-Off

Upon completing the review, please fill in the following:

| Field | Value |
|---|---|
| **Reviewer name** | _____ |
| **Reviewer role** | _____ |
| **Institution** | _____ |
| **Date** | _____ |
| **Signature** | _____ |

---

## Appendix: Glossary

| Term | Meaning |
|---|---|
| **ACT** | Artemisinin-based combination therapy |
| **NLL** | Natural Language Logic — human-readable representation of table logic |
| **Audit hash** | SHA-256 hash of extracted content; ensures tamper detection |
| **Preservation level** | Controls whether RAG/LLM may paraphrase: verbatim (no), high (minimal), standard (yes) |
| **Tier 1** | Dosing tables that passed all 6 automated plausibility checks |
| **Tier 2** | Dosing tables that were not validated by automated checks |
| **Tier 3** | Clinical management tables (safety-critical) |
| **Tier 4** | Evidence tables and narratives containing dosing/contraindication keywords |
| **G6PD** | Glucose-6-phosphate dehydrogenase (enzyme deficiency relevant to antimalarial safety) |
