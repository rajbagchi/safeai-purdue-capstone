# Uganda Clinical Guidelines 2023 pipeline run report

- **Generated (UTC)**: 2026-03-20T00:08:38.762362+00:00
- **Preset**: uganda (MoH Clinical Guidelines 2023)
- **PDF**: `C:\temp\capstone\Uganda Clinical Guidelines 2023.pdf`
- **KB output directory**: `C:\temp\capstone\medical_kb_uganda_clinical_2023`
- **Reuse KB flag**: `False`

---
## Stage 1: Multi-pass extraction

| Metric | Value |
|--------|-------|
| PDF path | `C:\temp\capstone\Uganda Clinical Guidelines 2023.pdf` |
| Extraction timestamp | 2026-03-19T19:08:33.693748 |
| Total pages extracted | 1161 |
| Tables extracted | 950 |
| Embedded images saved | 43 |
| OCR / manual-review flags | 0 |
| Cross-validation method | pdfplumber |
| Cross-validation consistency score | 0.9081618439234158 |
| Passes logged | 5 |

### Extraction passes

| Pass | Strategy | Details |
|------|----------|---------|
| 0 | `analysis` | `{"pass": 0, "strategy": "analysis", "profile_pages_sample": "[{'page': 1, 'text_length': 140, 'has_images': True, 'has_vector_graphics': True"}` |
| 1 | `text_extraction` | `{"pass": 1, "strategy": "text_extraction", "pages": 1161}` |
| 2 | `table_extraction` | `{"pass": 2, "strategy": "table_extraction", "tables_found": 950}` |
| 4 | `cross_validation` | `{"pass": 4, "strategy": "cross_validation", "results": {"method": "pdfplumber", "page_matches": [{"page": 1, "similarity": 0.9819494584837546}, {"page": 2, "similarity": 0.9928970065956367}, {"page": 3, "similarity": 0.9855564995751912}, {"` |
| images | `embedded_raster` | `{"pass": "images", "strategy": "embedded_raster", "images_saved": 43}` |

## Stage 2: Validation

### Overall

- **Passed (threshold)**: False
- **Confidence**: 72.16%
- **Needs human review**: True

### Structure

```json
{
  "stage": "structure",
  "passed": false,
  "issues": [
    "Heading level skipped: 1 \u2192 3"
  ],
  "confidence": 0.7,
  "suggestions": [
    "Verify heading hierarchy manually"
  ],
  "metadata": {
    "pages_extracted": 1161
  }
}
```

### Tables

```json
{
  "stage": "tables",
  "passed": true,
  "issues": [
    "Possible dosing table on page 58 has few numeric values",
    "Possible dosing table on page 59 has few numeric values",
    "Possible dosing table on page 109 has few numeric values",
    "Possible dosing table on page 177 has few numeric values",
    "Possible dosing table on page 225 has few numeric values",
    "Possible dosing table on page 276 has few numeric values",
    "Possible dosing table on page 319 has few numeric values",
    "Possible dosing table on page 373 has few numeric values",
    "Possible dosing table on page 556 has few numeric values",
    "Possible dosing table on page 697 has few numeric values",
    "Possible dosing table on page 889 has few numeric values",
    "Possible dosing table on page 889 has few numeric values"
  ],
  "confidence": 1.0,
  "suggestions": [],
  "metadata": {
    "tables_extracted": 950,
    "valid_tables": 950
  }
}
```

### Cross

```json
{
  "stage": "cross_consistency",
  "passed": true,
  "issues": [],
  "confidence": 0.9081618439234158,
  "suggestions": [],
  "metadata": {
    "consistency_score": 0.9081618439234158
  }
}
```

### Medical

```json
{
  "stage": "medical_content",
  "passed": true,
  "issues": [],
  "confidence": 1.0,
  "suggestions": [],
  "metadata": {
    "terms_found": [
      "dose",
      "mg",
      "treatment",
      "diagnosis",
      "patient",
      "child",
      "adult",
      "contraindication",
      "referral",
      "hospital",
      "symptom"
    ],
    "terms_missing": []
  }
}
```

### Human Review

```json
{
  "stage": "human_review",
  "passed": false,
  "issues": [
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
    "Dosing accuracy critical - requires human verification",
  
... (truncated)
```

## Stage 3: Chunking + BM25 index

| Metric | Value |
|--------|-------|
| Total chunks | 4222 |
| Chunks with tables | 3903 |

### Sample chunk headings (first 15)

- p.2 — **Foreword**
- p.3 — **Untitled**
- p.4 — **Introduction to Uganda Clinical Guidelines 2023.............................. XL**
- p.4 — **1.1 Common Emergencies..........................................................**
- p.4 — **1.2 Trauma and Injuries.........................................................**
- p.5 — **1.3 Poisoning...................................................................**
- p.5 — **2.1 Bacterial Infections........................................................**
- p.6 — **2.3 Viral Infections............................................................**
- p.6 — **2.4 Helminthes Parasites........................................................**
- p.6 — **2.5 Protozoal Parasites.........................................................**
- p.6 — **3.1 HIV Infection And Acquired Immunodeficiency Syndrome (AIDS)  .186**
- p.7 — **Untitled**
- p.7 — **3.2 Sexually Transmitted Infections (STI).......................................**
- p.7 — **4 CARDIOVASCULAR DISEASES..................................................298**
- p.8 — **Untitled**

## Stage 4: Guardrail brain

`MedicalGuardrailBrain` validates each composed answer: triage headings, dangerous patterns, citations vs. chunk pages.

## Stage 5: Search & Q&A (25 queries)

BM25 top-5 excerpts per query; guardrail summary below each.

### 1. Query

> Integrated management of childhood illness pneumonia classification

**Sources (top hits)**
- Page 37: IPT
- Page 932: 17.4  INTEGRATED COMMUNITY CASE MANAGEMENT
- Page 878: Childhood Illness
- Page 879: Childhood Illness
- Page 897: Childhood Illness

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Integrated management of childhood illness pneumonia classification

### 1. IPT

### IPT

HBV

Hepatitis B Virus

HC

Health Centre

Hct/Ht

Haematocrit

HCW

Health Care Worker

HDU

High Dependency Unit

HE

Hepatic Encephalopathy

HepB

Hepatitis B

HHS

Hyperosmolar Hyperglycaemic State

Hib

Haemophilus Influenzae Type B

HIV

Human Immunodeficiency Virus

HPV

Human Papilloma Virus

HR

Heart Rate

HRP

High-Risk Pregnancy

HRS

Hepatorenal Syndrome

HSV

Herpes Simplex Virus

HVS

High Vaginal  Swab

ICCM

Integrated Community Case Management

ICU

Intensive Care  Uni...

📄 **Reference:** Page 37

### 2. 17.4  INTEGRATED COMMUNITY CASE MANAGEMENT

### 17.4  INTEGRATED COMMUNITY CASE MANAGEMENT

17.4  INTEGRATED COMMUNITY CASE MANAGEMENT

Integrated Community Case Management (iCCM) of malaria, pneumo­

nia and diarrhoea is a recently adopted strategy for the treatment of

common childhood illness at community level by trained Community

Health Workers since 2010. It addresses a gap in delivery of curative

services to children below 5 years allowing:



prompt and accessible treatment of uncomplicated malaria, pneu­

monia and diarrhoea

...

📄 **Reference:** Page 932

### 3. Childhood Illness

### Childhood Illness

Uganda Clinical Guidelines 2023

CHAPTER 17: Childhood Illness

-

Pinch the skin of the

abdomen. Does it go

back

-

Very slowly? (takes >2

seconds)

-

Slowly? (up to 2 seconds)...

📄 **Reference:** Page 878

### 4. Childhood Illness

### Childhood Illness

Uganda Clinical Guidelines 2023

CHAPTER 17: Childhood Illness

CLINICAL FEATURES

CLASSIFY AS

MANAGEMENT

~

Sunken

eyes



FOLLOW UP in 2 days:...

📄 **Reference:** Page 879

### 5. Childhood Illness

### Childhood Illness

Uganda Clinical Guidelines 2023

CHAPTER 17: Childhood Illness...

📄 **Reference:** Page 897


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 37, Page 878, Page 879, Page 897, Page 932

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 2. Query

> Diarrhea dehydration ORS zinc treatment plan

**Sources (top hits)**
- Page 75: Plan A (No dehydration and for prevention)
- Page 77: Plan C (Severe dehydration)
- Page 75: ORS
- Page 77: Emergencies and Trauma
- Page 75: Management

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Diarrhea dehydration ORS zinc treatment plan

### 1. Plan A (No dehydration and for prevention)

### Plan A (No dehydration and for prevention)

Plan A (No dehydration and for prevention)

TREATMENT

LOC



Counsel the mother on the 4 rules of home treatment:

extra fluids (ORS), continue feeding, zinc supplemen­

tation, when to return

HC2



Give extra fluids: as much as the child will take

- If child exclusively breastfed, give ORS or safe...

📄 **Reference:** Page 75

### 2. Plan C (Severe dehydration)

### Plan C (Severe dehydration)

Plan C (Severe dehydration)

TREATMENT

LOC...

📄 **Reference:** Page 77

### 3. ORS

### ORS

- In addition to the usual fluid intake, give ORS after

each loose stool or episode of vomiting Child <2

years: 50-100 ml

Child 2-5 years: 100-200 ml

- Give the mother 2 packets to use at home

- Giving ORS is especially important if the child

has been treated with Plan B or Plan C during

current visit

- Give frequent small sips from a cup



Advice the mother to continue or increase breastfeeding.

If child vomits, wait 10 minutes, then give more slowly

- In a child with high ...

📄 **Reference:** Page 75

### 4. Emergencies and Trauma

### Emergencies and Trauma

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

TREATMENT

LOC

If mother must leave before completing the child’s treatment



Show her how to prepare ORS at home and how much

ORS to give to finish the 4-hour treatment

- Give her enough packets to complete this and 2

more to complete Plan A at home



Counsel mother on the 4 rules of home treatment: extra

fluids, continue feeding, zinc, when to return...

📄 **Reference:** Page 77

### 5. Management

### Management

Management...

📄 **Reference:** Page 75


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 75, Page 77

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 3. Query

> HIV antiretroviral therapy first-line regimen adults

**Sources (top hits)**
- Page 444: ment regimen
- Page 444: Important:
- Page 444: Susceptible TB: 1st line treatment regimens
- Page 289: HIV/AIDS and Sexually Transmitted Infections
- Page 268: Principles of ART

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** HIV antiretroviral therapy first-line regimen adults

### 1. ment regimen

### ment regimen

Alternative 1st-line treat­

ment regimen

All forms of TB in children

(2 months to 16 years) with

non-severe disease

2 HRE(Z)

2RH

G e n e r a l

Hospital and

above

All forms of TB in adults

above 12 years, weight

>40 Kgs, if HIV positive

CD4>100 cells/L

2 HPMZ

2HPM

378...

📄 **Reference:** Page 444

### 2. Important:

### Important:

Important: The choice of regimen now depends on rifampicin

sensitivity and not on the previous history of treatment:



All patients without rifampicin resistance (either new or re-treat­

ments) are treated with 1st line regimen.



Patients with rifampicin resistance (either new or re- treatments)

are treated with second line medication in a designated MDR-TB

treatment facility....

📄 **Reference:** Page 444

### 3. Susceptible TB: 1st line treatment regimens

### Susceptible TB: 1st line treatment regimens

Susceptible TB: 1st line treatment regimens

For patients without rifampicin resistance to  Gene Xpert MTB/Rif (both

new and re-treatment cases).

New cases not belonging to priority (risk) groups and in which diagnosis

was done by sputum examination will also be treated with this regimen....

📄 **Reference:** Page 444

### 4. HIV/AIDS and Sexually Transmitted Infections

### HIV/AIDS and Sexually Transmitted Infections

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

orATV/r

All third line regimens

to be guided by HIV

the table to guide the

drug resistance test­

In case of suscepti­

preferred or alterna­

regimens1,2

to all drugs, use

line regimen

Third line

tive choices.

bility

ing....

📄 **Reference:** Page 289

### 5. Principles of ART

### Principles of ART

Principles of ART

~

Antiretroviral therapy is part of comprehensive HIV care.

The guiding principles of good ART include:

~

Efficacy and durability of the chosen medicine regimens

~

Freedom from serious adverse effects; low toxicity

~

Ease of administration including no food restrictions, better

palatability, and lower pill burden

~

Affordability and availability of medicines and medicine com­

binations

~

Organised sequencing – spares other available formula...

📄 **Reference:** Page 268


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 268, Page 289, Page 444

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 4. Query

> Tuberculosis treatment regimen and contact investigation

**Sources (top hits)**
- Page 166: Investigation
- Page 497: Investigation
- Page 452: 5.3.2.3	 Tuberculosis Preventive Treatment
- Page 320: HIV/AIDS and Sexually Transmitted Infections
- Page 451: Contact tracing

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Tuberculosis treatment regimen and contact investigation

### 1. Investigation

### Investigation

Investigation...

📄 **Reference:** Page 166

### 2. Investigation

### Investigation

Investigation...

📄 **Reference:** Page 497

### 3. 5.3.2.3	 Tuberculosis Preventive Treatment

### 5.3.2.3	 Tuberculosis Preventive Treatment

5.3.2.3	 Tuberculosis Preventive Treatment

Tuberculosis preventive treatment is recommended to prevent the

development of active TB disease in an individual who has latent TB

infection (LTBI).

Uganda  guidelines for programmatic management of Latent TB infection

recommend TB preventive treatment (TPT ) in the following categories

of people:

- Persons living with HIV

- Child & adult contacts of pulmonary TB patients

Do not use TPT in cases ...

📄 **Reference:** Page 452

### 4. HIV/AIDS and Sexually Transmitted Infections

### HIV/AIDS and Sexually Transmitted Infections

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

ARV regimen substitution for patients initiating TB treatment while on ART

Age Group

Regimen When Di­

agnosed With Tb

Recommended Action/ Sub­

stitution

Adults, Preg­

n a n t  a n d

Breastfeeding

Women and

Adolescents

If on LPV/r based

regimen

Continue the same regimen but

double the dose of DTG (give

DTG twice daily)

If on ATV/r based

regim...

📄 **Reference:** Page 320

### 5. Contact tracing

### Contact tracing

Contact tracing

~

Tracing of contacts of TB patients

~

Routine screening of health workers for latent & active TB...

📄 **Reference:** Page 451


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 166, Page 320, Page 451, Page 452, Page 497

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 5. Query

> Malaria uncomplicated case management ACT dosing children

**Sources (top hits)**
- Page 235: Treatment of uncomplicated malaria
- Page 235: Management of Malaria
- Page 775: Management of Malaria in Pregnancy
- Page 235: Infectious Diseases
- Page 932: 17.4  INTEGRATED COMMUNITY CASE MANAGEMENT

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Malaria uncomplicated case management ACT dosing children

### 1. Treatment of uncomplicated malaria

### Treatment of uncomplicated malaria

Treatment of uncomplicated malaria

The following tables contain dosages for medicines used in treatment of

uncomplicated malaria.

169...

📄 **Reference:** Page 235

### 2. Management of Malaria

### Management of Malaria

Management of Malaria

NATIONAL MALARIA TREATMENT POLICY

Uncomplicated Malaria

All patients: including children

<4 months of age and pregnant

women

in 2nd and 3rd trimesters

First line medicine

Artemether/Lumefantrine

First line alternative

Artesunate/Amodiaquine

Second line medicine

Dihydroartemisin/ Piperaquine

If not available: quinine tablets

Pregnant women 1st trimester

ACT currently used

Severe Malaria

All age groups or patient categories First li...

📄 **Reference:** Page 235

### 3. Management of Malaria in Pregnancy

### Management of Malaria in Pregnancy

Management of Malaria in Pregnancy

APPROACH

MANAGEMENT

LOC

Prophylaxis All

pregnant mothers

Wexcept those

with HIV on

cotrimoxazole

prophylaxis



Intermittent Preventive Treatment

(IPTp) with Sulphadoxine/ pyrimeth­

amine (SP) once a month starting

at 13 weeks until delivery

HC2



Quinine oral 600 mg 8 hourly for 7

days (if Quinine not available, ACT

may be used)

Treatment of

Uncomplicated

malaria in 1st

trimester

HC2

709...

📄 **Reference:** Page 775

### 4. Infectious Diseases

### Infectious Diseases

Uganda Clinical Guidelines 2023

CHAPTER 2: Infectious Diseases...

📄 **Reference:** Page 235

### 5. 17.4  INTEGRATED COMMUNITY CASE MANAGEMENT

### 17.4  INTEGRATED COMMUNITY CASE MANAGEMENT

17.4  INTEGRATED COMMUNITY CASE MANAGEMENT

Integrated Community Case Management (iCCM) of malaria, pneumo­

nia and diarrhoea is a recently adopted strategy for the treatment of

common childhood illness at community level by trained Community

Health Workers since 2010. It addresses a gap in delivery of curative

services to children below 5 years allowing:



prompt and accessible treatment of uncomplicated malaria, pneu­

monia and diarrhoea

...

📄 **Reference:** Page 932


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 235, Page 775, Page 932

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 6. Query

> Postpartum hemorrhage emergency management oxytocin

**Sources (top hits)**
- Page 789: and no signs of infection
- Page 812: 16.4.6 Postpartum Haemorrhage (PPH)
- Page 789: Obstetric Conditions
- Page 837: Check for vaginal bleeding and possible uterine/urinary tract or febrile infection
- Page 807: Cervix not favourable

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Postpartum hemorrhage emergency management oxytocin

### 1. and no signs of infection

### and no signs of infection

If the membranes have been ruptured for >18 hours

and no signs of infection



Give prophylactic antibiotics until delivery to help reduce

neonatal group B streptococcus infection: Ampicillin 2

g IV every 6 hours or benzylpenicillin 2 MU IV every

6 hours

HC4



Assess the cervix



Refer to HC4 or above (with facilities for emergency

obstetric management) for induction with oxytocin (see

section 16.4.2)...

📄 **Reference:** Page 789

### 2. 16.4.6 Postpartum Haemorrhage (PPH)

### 16.4.6 Postpartum Haemorrhage (PPH)

16.4.6 Postpartum Haemorrhage (PPH)    ICD10 CODE: O72

Vaginal bleeding of more than 500 mL after vaginal delivery or >1000

mL after caesarean section.

746...

📄 **Reference:** Page 812

### 3. Obstetric Conditions

### Obstetric Conditions

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

MANAGEMENT

LOC



Refer all patients to hospital and keep in hospital until

delivery

HC4...

📄 **Reference:** Page 789

### 4. Check for vaginal bleeding and possible uterine/urinary tract or febrile infection

### Check for vaginal bleeding and possible uterine/urinary tract or febrile infection

Check for vaginal bleeding and possible uterine/urinary tract or febrile infection

otics

months

Postpartum

Postpartum

Moderate

No Anae­

6 weeks

minutes

bleeing

delivery

soaked

1 pad

bleeding



More

than

after

in 5



Still



Hb 7-11



Hb >11

g/dL or



Palmar

juctival­

or con­

pallor

pallor

g/dL



No



Heavy vaginal

vaginal bleed­



Heavy/ light

ing after 6



Look for

...

📄 **Reference:** Page 837

### 5. Cervix not favourable

### Cervix not favourable

Cervix not favourable



Ripen cervix using either



Misoprostol 25 micrograms inserted vaginally every

6 hours for 2 doses, if no response increase to 50

micrograms every 6 hours, max 200 micrograms in

24 hours – stop when in established labour



Or misoprostol 20 micrograms orally (dissolve 1 200

microgram tablet in 200 mL of water and give 20 mL)

every 2 hours until labour starts or max 24 hours



Or Foley catheter: insert Foley catheter through internal...

📄 **Reference:** Page 807


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 789, Page 807, Page 812, Page 837

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 7. Query

> Family planning contraceptive counseling methods

**Sources (top hits)**
- Page 751: Family Planning (FP)
- Page 725: 15.1.10  Summary of Medical Eligibility for Contraceptives
- Page 730: 15.2  Overview Of Key Contraceptive Methods
- Page 730: Methods all couples (except a few) can safely use
- Page 1062: Oral contraceptives

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Family planning contraceptive counseling methods

### 1. Family Planning (FP)

### Family Planning (FP)

Uganda Clinical Guidelines 2023

CHAPTER 15: Family Planning (FP)

INSTRUCTIONS

LOC...

📄 **Reference:** Page 751

### 2. 15.1.10  Summary of Medical Eligibility for Contraceptives

### 15.1.10  Summary of Medical Eligibility for Contraceptives

15.1.10  Summary of Medical Eligibility for Contraceptives

The tables below contain a ummarized version of the medical eligibility

criteria for initiating a patient on contraceptive methods, based on the

MOH (2016) and WHO (2020) Medical Eligibility Criteria for Contracep­

tive Use. It guides family planning providers in recommending safe and

effective contraception methods for women with medical conditions or

medially-relevan...

📄 **Reference:** Page 725

### 3. 15.2  Overview Of Key Contraceptive Methods

### 15.2  Overview Of Key Contraceptive Methods

15.2  Overview Of Key Contraceptive Methods

The following sections contain an overview of mainstream contraceptive

methods and how to manage side effects

of each (in case they occur). Side effects are one of most common reasons

why women stop using contraception, and the health worker should

be able to counsel the patient and address her concerns appropriately....

📄 **Reference:** Page 730

### 4. Methods all couples (except a few) can safely use

### Methods all couples (except a few) can safely use

Methods all couples (except a few) can safely use

Emergency contraceptive pill (for emergency use only) Bilateral Tubal

Ligation (BTL) and Vasectomy

Barrier methods (condoms, diaphragm) Lactational amenorrhoea

method (LAM)

Fertility awareness (FAM) and Standard days methods...

📄 **Reference:** Page 730

### 5. Oral contraceptives

### Oral contraceptives

Oral contraceptives



Combined oral contraceptive (see Family Planning,

section 15.2.3)...

📄 **Reference:** Page 1062


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 725, Page 730, Page 751, Page 1062

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 8. Query

> Hypertension diagnosis and management primary care

**Sources (top hits)**
- Page 54: Chronic Care
- Page 830: Postpartum care services
- Page 296: Management
- Page 1046: Differential diagnosis
- Page 995: Management

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Hypertension diagnosis and management primary care

### 1. Chronic Care

### Chronic Care

Chronic Care

~

Health workers are faced with an increasing number of

chronic diseases and conditions that require additional at­

tention, such as hypertension, chronic heart problems, dia­

betes, cancers, mental conditions, HIV/AIDS, and TB.

~

Communication is even more important to:

~

Find out the duration of the symptoms, previous diagnosis,

previous or current treatments and impact on daily life

~

Explain the nature and management of the condition to the

patient...

📄 **Reference:** Page 54

### 2. Postpartum care services

### Postpartum care services

Postpartum care services

The mother and baby should be seen at 6 hours after birth and again

before discharge if in a health facility (and anytime the mother reports

concern about herself and her baby) or approximately 6 hours after

delivery at home.

The routine follow-up visits are at 6 days and 6 weeks, and have the

following components:



Counselling



Assessment and management of observed or reported prob­

lems. Check for hypertension, anaemia, vagina...

📄 **Reference:** Page 830

### 3. Management

### Management

Management

All HIV services for pregnant mothers are offered in the MCH clinic.

After delivery, mother and baby will remain in the MCH postnatal clinic

till HIV status of the child is

confirmed, then they will be transferred to the general ART clinic.

The current policy aims at elimination of Mother-to-Child Transmission

(eMTCT) through provision of a continuum of care with the following

elements:

- Primary HIV prevention for men, women and adolescents

- Prevention of un...

📄 **Reference:** Page 296

### 4. Differential diagnosis

### Differential diagnosis

Differential diagnosis

~

Aphthous ulcer

~

Other causes of genital sores, e.g., syphilis

~

Other causes of meningoencephalitis...

📄 **Reference:** Page 1046

### 5. Management

### Management



Investigation of uveitis is broad and requires a high index of

suspicion



Diagnosis of uveitis requires expertise and can only be confirmed

by slit lamp examinations

Management

TREATMENT

LOC

If at HC2 and HC3...

📄 **Reference:** Page 995


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 54, Page 296, Page 830, Page 995, Page 1046

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 9. Query

> Diabetes mellitus type 2 glycemic targets

**Sources (top hits)**
- Page 778: Therapeutic targets
- Page 537: Diabetes Mellitus
- Page 541: Treatment targets
- Page 721: 15.1.6  Obtain and Record Client History
- Page 10: 8 ENDOCRINE AND METABOLIC DISEASES..................................468

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Diabetes mellitus type 2 glycemic targets

### 1. Therapeutic targets

### Therapeutic targets

Therapeutic targets

~

Pre prandial blood glucose <5.3 mmol/L

~

1-hour postprandial glucose <7.8 mmol/L

~

2-hour postprandial glucose <6.4 mmol/L...

📄 **Reference:** Page 778

### 2. Diabetes Mellitus

### Diabetes Mellitus

8.1.3

Diabetes Mellitus

ICD10 CODE: E08-E13

Metabolic disease resulting from insulin insufficiency or ineffectiveness,

due to decreased insulin secretion, or peripheral resistance to the action

of insulin, or a combination of the two....

📄 **Reference:** Page 537

### 3. Treatment targets

### Treatment targets

Treatment targets

- Fasting blood sugar <7 mmol/l

- Postprandial sugar <10 mmol/l

- HbA1c <7% (7.5 % for elderly)

Elderly people are at higher risk of hypoglycaemia. Monitor carefully,

and do not aim at very strict control of blood sugar.

Management of Type 1 Diabetes

Insulin SC: 0.6 -1.5 IU/kg/day HC4 Children <5 years: start with 0.5

IU/Kg/day, and refer to a paediatrician

Type of

Usual

Action

Onset

Peak

Duration

Insulin

Protocol

Insulin short

acting, r...

📄 **Reference:** Page 541

### 4. 15.1.6  Obtain and Record Client History

### 15.1.6  Obtain and Record Client History

15.1.6  Obtain and Record Client History

The primary objectives are:

~

To obtain client’s personal and social data and information

on health status

~

To identify abnormalities/problems requiring treatment or

referral

For FP clients, it is important to pay particular attention to information

outlined in the table below:

HISTORY

INFORMATION NEEDED

Social History

~

Smoking? How many ummarized per

day?

~

Drinking? How much alcohol per da...

📄 **Reference:** Page 721

### 5. 8 ENDOCRINE AND METABOLIC DISEASES..................................468

### 8 ENDOCRINE AND METABOLIC DISEASES..................................468

8 ENDOCRINE AND METABOLIC DISEASES..................................468

8.1.1 Addison’s Disease..........................................................................................468

8.1.2 Cushing’s Syndrome.......................................................................................470

8.1.3 Diabetes Mellitus............................................................................................4...

📄 **Reference:** Page 10


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 10, Page 537, Page 541, Page 721, Page 778

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 10. Query

> Acute stroke referral and supportive care

**Sources (top hits)**
- Page 394: If stroke clinically haemorrhagic
- Page 394: Chronic care of ischaemic stroke
- Page 394: If ischaemic stroke
- Page 394: Cardiovascular Diseases
- Page 394: Management of stable angina

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Acute stroke referral and supportive care

### 1. If stroke clinically haemorrhagic

### If stroke clinically haemorrhagic

If stroke clinically haemorrhagic



Supportive care as above



Refer for CT scan and neurosurgical evaluation...

📄 **Reference:** Page 394

### 2. Chronic care of ischaemic stroke

### Chronic care of ischaemic stroke

Chronic care of ischaemic stroke



Early mobilization and physiotherapy f Aspirin 75-100

mg once daily for life f Atorvastatin 40 mg daily for life



Control of risk factors

328...

📄 **Reference:** Page 394

### 3. If ischaemic stroke

### If ischaemic stroke

If ischaemic stroke

H



Aspirin 150-300 mg every 24 hours



In the acute phase, treat hypertension only if extreme

(more than 220/120) or if there are other complications

(pulmonary oedema, angina, etc), otherwise re-start

antihypertensive 24 hours after the event and reduce

blood pressure slowly



Consider DVT prophylaxis with enoxaparin 40 mg

SC daily...

📄 **Reference:** Page 394

### 4. Cardiovascular Diseases

### Cardiovascular Diseases

Uganda Clinical Guidelines 2023

CHAPTER 4: Cardiovascular Diseases...

📄 **Reference:** Page 394

### 5. Management of stable angina

### Management of stable angina

Management of stable angina

TREATMENT

LOC...

📄 **Reference:** Page 394


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 394

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 11. Query

> Syndromic management sexually transmitted infections

**Sources (top hits)**
- Page 343: HIV/AIDS and Sexually Transmitted Infections
- Page 317: HIV/AIDS and Sexually Transmitted Infections
- Page 349: HIV/AIDS and Sexually Transmitted Infections
- Page 346: HIV/AIDS and Sexually Transmitted Infections
- Page 356: HIV/AIDS and Sexually Transmitted Infections

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Syndromic management sexually transmitted infections

### 1. HIV/AIDS and Sexually Transmitted Infections

### HIV/AIDS and Sexually Transmitted Infections

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections...

📄 **Reference:** Page 343

### 2. HIV/AIDS and Sexually Transmitted Infections

### HIV/AIDS and Sexually Transmitted Infections

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections...

📄 **Reference:** Page 317

### 3. HIV/AIDS and Sexually Transmitted Infections

### HIV/AIDS and Sexually Transmitted Infections

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

TREATMENT

LOC...

📄 **Reference:** Page 349

### 4. HIV/AIDS and Sexually Transmitted Infections

### HIV/AIDS and Sexually Transmitted Infections

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

Candida vaginitis and bacterial vaginosis are NOT sexually transmitted

diseases, even though sexual activity is a risk factor.

~

Gonorrhoea causes cervicitis and rarely vaginitis. Thereis a

purulent thin mucoid slightly yellow pus discharge with no

smell and non-itchy

~

Chlamydia causes cervicitis which may present with a non-

itchy, thin, colourless...

📄 **Reference:** Page 346

### 5. HIV/AIDS and Sexually Transmitted Infections

### HIV/AIDS and Sexually Transmitted Infections

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

TREATMENT

LOC...

📄 **Reference:** Page 356


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 317, Page 343, Page 346, Page 349, Page 356

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 12. Query

> Cervical cancer screening VIA HPV

**Sources (top hits)**
- Page 677: Screening for Cervical Cancer
- Page 675: Prevention of Infections
- Page 674: Oncogenic Infections
- Page 677: owing if using VIA as a screening method:
- Page 676: Oncology

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Cervical cancer screening VIA HPV

### 1. Screening for Cervical Cancer

### Screening for Cervical Cancer

Screening for Cervical Cancer

This aims to detect pre-cancerous lesions that are then treated to prevent

progression to invasive cancer. The following methods are recommended:

Visual Inspection with Acetic Acid (VIA): involves applying 3-5% freshly

prepared acetic acid to the cervix and observing results after one minute.

 The VIA results are generally categorized into 3 subsets:

suspicious for cancer, VIA negative and VIA positive

 It uses readily ava...

📄 **Reference:** Page 677

### 2. Prevention of Infections

### Prevention of Infections

Prevention of Infections

The following infections are associated with causing certain types of

cancer:

~

Viral Hepatitis B/C: cancer of the liver

~

Human Papilloma Virus (HPV): cervical cancer

~

Helicobacter Pylori: stomach cancer

HIV/AIDS: aggressive lymphoma subtypes, Kaposi’s sarcoma, anorectal

cancer, cervical cancer, etc

~

Schistosomiasis: increases risk of bladder cancer

~

Liver Fluke: increases risk of cholangio-carcinoma

~

Preventative measur...

📄 **Reference:** Page 675

### 3. Oncogenic Infections

### Oncogenic Infections

Oncogenic Infections

The following infections are associated with causing certain types of

cancer:

 Viral Hepatitis B/C: cancer of the liver

 Human Papilloma Virus (HPV): cervical, oral, anal, and cancer

 Helicobacter Pylori: Gastric (stomach) cancer

 HIV/AIDS: aggressive lymphoma subtypes, Kaposi’s sarcoma,

anorectal cancer, cervical cancer, etc.

 Schistosomiasis: increases risk of bladder cancer

 Liver Fluke: increases risk of cholangio-carcinoma

 Pre...

📄 **Reference:** Page 674

### 4. owing if using VIA as a screening method:

### owing if using VIA as a screening method:

Consider the following if using VIA as a screening method:

 Women <25 years of age should be screened only if they are

at high risk for disease: HIV positive, early sexual exposure,

multiple partners, previous abnormal screening results, cervical

intraepithelial neoplasia (CIN)

 VIA is not appropriate for women >50 years

 Screening is advised every 3-5 years in case of normal results,

but after 1 years in case of abnormal results and treat...

📄 **Reference:** Page 677

### 5. Oncology

### Oncology

Uganda Clinical Guidelines 2023

CHAPTER 12: Oncology

ing, early diagnosis, pre-cancer treatment or cancer management, and

referral to avoid or reduce complications associated with the cancer.

Secondary prevention strategies relate to the discovery and control of

cancerous or pre-cancerous lesions.

Early detection of cancer greatly increases the chances for successful

treatment and cure. It comprises of:

~

Early diagnosis in symptomatic populations

~

Screening in asymptom...

📄 **Reference:** Page 676


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 674, Page 675, Page 676, Page 677

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 13. Query

> Routine immunization schedule infants Uganda

**Sources (top hits)**
- Page 16: 18.1  Routine Childhood Vaccination...............................................875
- Page 305: HIV/AIDS and Sexually Transmitted Infections
- Page 305: 3.1.9.2 HIV-exposed infant care services
- Page 889: Check immunization card and classify
- Page 423: Prevention

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Routine immunization schedule infants Uganda

### 1. 18.1  Routine Childhood Vaccination...............................................875

### 18.1  Routine Childhood Vaccination...............................................875

18 IMMUNIZATION......................................................................875

18.1  Routine Childhood Vaccination...............................................875

18.1.1   National Immunization Schedule.................................................................875

18.1.2  Hepatitis B Vaccination...............................................................................881

18.1.3  ...

📄 **Reference:** Page 16

### 2. HIV/AIDS and Sexually Transmitted Infections

### HIV/AIDS and Sexually Transmitted Infections

Uganda Clinical Guidelines 2023

CHAPTER 3: HIV/AIDS and Sexually Transmitted Infections

Service

Description

• 8 ANC visits

• Two weeks after

initiating ART

• Synchronize ART

refills and adherence

support with the ANC

visits

• After that, monthly

until delivery

• Follow routine

MCH schedule after

delivery together

with the exposed

infant visit schedule...

📄 **Reference:** Page 305

### 3. 3.1.9.2 HIV-exposed infant care services

### 3.1.9.2 HIV-exposed infant care services

3.1.9.2 HIV-exposed infant care services

Service

Description

Identification of

HIV-exposed in­

fants

• Identify all HIV-exposed infants; document the

HIV status of the mother in the child card and

mothers’ passport. Infants whose HIV status

is not documented or is unknown should be

offered rapid HIV testing; including those whose

mothers did not receive eMTCT services or have

become newly infected after pregnancy. Rapid

diagnostic tests ...

📄 **Reference:** Page 305

### 4. Check immunization card and classify

### Check immunization card and classify

Check immunization card and classify

~

Imuniza­

tion not

up to date

according

~

to national

schedule

(see chap­

ter 18)

~

Give all missed

doses on this

visit (Include sick

infants unless

being referred)

Infant Not

Immunized

as per

Schedule

~

Immuniza­

tion upto

date as per

national

schedule

~

Advise caretaker

when to return

for the next

dose

Infant Im­

munized as

Per Sched­

ule...

📄 **Reference:** Page 889

### 5. Prevention

### Prevention

Prevention

~

Educate parents on the importance of following the routine

childhood immunisation schedule:

~

Ensure good nutrition

~

Avoid overcrowding

~

Booster doses of vaccine in exposed infants...

📄 **Reference:** Page 423


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 16, Page 305, Page 423, Page 889

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 14. Query

> Severe acute malnutrition inpatient management

**Sources (top hits)**
- Page 17: 19.2  Malnutrition.........................................................................890
- Page 959: 19.2.1.2  Assessing Malnutrition in Children 6 months to 5 years
- Page 963: 19.2.2   Management of Acute Malnutrition in Children
- Page 934: Weight for-Height/Length
- Page 963: 19.2.2.1   Management of Moderate Acute Malnutrition

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Severe acute malnutrition inpatient management

### 1. 19.2  Malnutrition.........................................................................890

### 19.2  Malnutrition.........................................................................890

19.2  Malnutrition.........................................................................890

19.2.1  Introduction on Malnutrition........................................................................890

19.2.1.1 Classification of Malnutrition......................................................................892

19.2.1.2 Assessing Malnutrition in Children 6 months to 5 years.................

📄 **Reference:** Page 17

### 2. 19.2.1.2  Assessing Malnutrition in Children 6 months to 5 years

### 19.2.1.2  Assessing Malnutrition in Children 6 months to 5 years

19.2.1.2  Assessing Malnutrition in Children 6 months to 5 years

The 4 key features used to diagnose acute malnutrition are:



Weight-for-Height/Length (WFH/L) using WHO growth standards

charts (see section 15.5). It is the best indicator for diagnosing

acute malnutrition.



Mean Upper Arm Circumference (MUAC) in mm using a measuring

tape (see section 17.5)



Oedema of both feet (kwashiorkor with or without severe wa...

📄 **Reference:** Page 959

### 3. 19.2.2   Management of Acute Malnutrition in Children

### 19.2.2   Management of Acute Malnutrition in Children

19.2.2   Management of Acute Malnutrition in Children...

📄 **Reference:** Page 963

### 4. Weight for-Height/Length

### Weight for-Height/Length

Weight for-Height/Length

r

Used to diagnose acute malnutrition

r

The cut-off for severe acute malnutrition is -3 z-scores and be­

low. These children are at a high risk of mortality, but respond

quickly and safely to re-feeding using therapeutic foods following

recommended guidelines.

r

The cut-off for moderate acute malnutrition is -2 to -3 z-scores

below.

868...

📄 **Reference:** Page 934

### 5. 19.2.2.1   Management of Moderate Acute Malnutrition

### 19.2.2.1   Management of Moderate Acute Malnutrition

19.2.2.1   Management of Moderate Acute Malnutrition

TREATMENT

LOC



Assess the child’s feeding and counsel the mother on

the feeding recommendations



If child has any feeding problem, counsel and follow up

in 7 days (see section 17.3.12.4)...

📄 **Reference:** Page 963


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 17, Page 934, Page 959, Page 963

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 15. Query

> Tuberculosis preventive therapy isoniazid

**Sources (top hits)**
- Page 37: IPT
- Page 316: TB preventive therapy (TPT)
- Page 452: 5.3.2.3	 Tuberculosis Preventive Treatment
- Page 454: 5.3.2.5	 TB Preventive Treatment Dosing Chart
- Page 264: TPT (TB Preventive treatment)

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Tuberculosis preventive therapy isoniazid

### 1. IPT

### IPT

HBV

Hepatitis B Virus

HC

Health Centre

Hct/Ht

Haematocrit

HCW

Health Care Worker

HDU

High Dependency Unit

HE

Hepatic Encephalopathy

HepB

Hepatitis B

HHS

Hyperosmolar Hyperglycaemic State

Hib

Haemophilus Influenzae Type B

HIV

Human Immunodeficiency Virus

HPV

Human Papilloma Virus

HR

Heart Rate

HRP

High-Risk Pregnancy

HRS

Hepatorenal Syndrome

HSV

Herpes Simplex Virus

HVS

High Vaginal  Swab

ICCM

Integrated Community Case Management

ICU

Intensive Care  Uni...

📄 **Reference:** Page 37

### 2. TB preventive therapy (TPT)

### TB preventive therapy (TPT)

TB preventive therapy (TPT)



Give INH for six months to HIV-exposed infant who

are exposed to TB (close contact with PTB case) after

excluding TB disease (see section 5.3.2.3)



Dose: Isoniazid 10 mg/kg + pyridoxine 25 mg daily



For newborn infants, if the mother has TB disease and

has been on anti-TB drugs for at least two weeks before

delivery, INH prophylaxis is not required.

250...

📄 **Reference:** Page 316

### 3. 5.3.2.3	 Tuberculosis Preventive Treatment

### 5.3.2.3	 Tuberculosis Preventive Treatment

5.3.2.3	 Tuberculosis Preventive Treatment

Tuberculosis preventive treatment is recommended to prevent the

development of active TB disease in an individual who has latent TB

infection (LTBI).

Uganda  guidelines for programmatic management of Latent TB infection

recommend TB preventive treatment (TPT ) in the following categories

of people:

- Persons living with HIV

- Child & adult contacts of pulmonary TB patients

Do not use TPT in cases ...

📄 **Reference:** Page 452

### 4. 5.3.2.5	 TB Preventive Treatment Dosing Chart

### 5.3.2.5	 TB Preventive Treatment Dosing Chart

5.3.2.5	 TB Preventive Treatment Dosing Chart

Medicine frequency

& duration

Formulation

Dose of TPT

medicine

(mgs)

Dose/

weight

Recom

3HP (once weekly

rifapentine plus isoni­

azid for 3 months)

Fixed Doze

Combination

(FDC) Tablet

Rifapentine

300mg/ Iso­

niazid 300mg

3–5.9

Single medicine

Pyridoxine

25mg/day

tablet

6H (daily isoniazid

for 6 months)

3–5.9

kgs

Isoniazid 100

mg

<10 years

0.5

Single medicine

10mg/kg

...

📄 **Reference:** Page 454

### 5. TPT (TB Preventive treatment)

### TPT (TB Preventive treatment)

TPT (TB Preventive treatment)

HC3



such as;   isoniazid + rifapentine(3HP)  weekly for 3

months in all adults, adolescents and children >12

months living with HIV and in whom TB disease has

been excluded (other medications for TPT refer to the

current HIV/TB guidelines)



If child <12 months, give only if history of contact with

TB case and no active disease (one-month daily rifap­

entine and isoniazid (1HP).)

– Dose:  (see section 5.3.2.1 )...

📄 **Reference:** Page 264


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 37, Page 264, Page 316, Page 452, Page 454

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 16. Query

> Depression screening and management primary care

**Sources (top hits)**
- Page 719: ceive
- Page 676: Screening for Breast Cancer
- Page 214: COVID-19 screening and triage process at health facilities
- Page 357: Investigations
- Page 759: 16.1  ANTENATAL CARE (ANC)

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Depression screening and management primary care

### 1. ceive

### ceive

ceive

Pre-conception care discussion topics for clients who desire to conceive

include:

~

Pregnancy planning and appropriate contraception

~

Folic acid supplementation 3 months preceeding concep­

tion

~

Good diet, risk assessment and management of pre exist­

ing conditions and risk factors

~

Benefits of preconception care (e.g., prevention of unin­

tended pregnancies, good maternal and foetal outcomes)

~

Screening for hereditary diseases e.g., sickle cell disease

~

Sc...

📄 **Reference:** Page 719

### 2. Screening for Breast Cancer

### Screening for Breast Cancer

Screening for Breast Cancer

Screening / health checkup for breast cancer involves:

Breast Self-Examination (BSE): a simple, quick examination done by the

client herself, aimed at early detection of lumps. Regular (monthly-not

during menstruation, at least seven days after ending the menstruation)

and correct technique of breast examination is important and easy to

teach and administer. Health workers should note that BSE is not a

standard screening test fo...

📄 **Reference:** Page 676

### 3. COVID-19 screening and triage process at health facilities

### COVID-19 screening and triage process at health facilities

COVID-19 screening and triage process at health facilities

~

COVID-19 triage aims to flag suspected patients at first

point of contact within the healthcare system in order to

~

protect other patients and staff from potential exposure.

~

identify and rapidly address severe symptoms, rule out oth­

er conditions with features similar to COVID-19, ascertain

if suspect case definition is met

~

All suspected patients should be...

📄 **Reference:** Page 214

### 4. Investigations

### Investigations

Investigations



Non-treponemal antibody tests (VDRL and RPR)

- Positive 4-6 weeks after infection

- Used as screening test

- Possibility of false positive

- Remains positive 6-12 months after treatment



Treponemal antibody tests (TPHA): very sensitive, used to confirm

a positive non-treponemal test. Remains positive for long even

after treatment so its positivity may not indicate active disease....

📄 **Reference:** Page 357

### 5. 16.1  ANTENATAL CARE (ANC)

### 16.1  ANTENATAL CARE (ANC)

16.1  ANTENATAL CARE (ANC)     ICD10 CODE: Z36

Antenatal care is a planned programme of medical care offered to

pregnant women by a skilled birth attendant, from the time of con­

ception to delivery, aimed at ensuring a safe and satisfying pregnancy

and birth outcome.

The main objective of antenatal care is to give information on:

~

Screening, prevention, and treatment of complications

~

Emergency preparedness

~

Birth planning

~

Satisfying any unmet n...

📄 **Reference:** Page 759


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 214, Page 357, Page 676, Page 719, Page 759

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 17. Query

> Asthma chronic management inhaler technique

**Sources (top hits)**
- Page 403: Chronic Asthma
- Page 403: General principles of management
- Page 402: Respiratory Diseases
- Page 403: STEP 1: Intermittent asthma
- Page 405: Caution

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Asthma chronic management inhaler technique

### 1. Chronic Asthma

### Chronic Asthma

5.1.1.2	 Chronic Asthma...

📄 **Reference:** Page 403

### 2. General principles of management

### General principles of management

General principles of management

~

Follow a stepped approach



Before initiating a new drug, check that diagnosis is correct, compli­

ance and inhaler technique are correct and eliminate trigger factors

for acute exacerbations

~

Start at the step most appropriate to initial severity

~

Rescue course



Give a 3-5 days “rescue course” of prednisolone at any step and

at any time as required to control acute exacerbations of asthma

at a dose of:

Ch...

📄 **Reference:** Page 403

### 3. Respiratory Diseases

### Respiratory Diseases

Uganda Clinical Guidelines 2023

CHAPTER 5: Respiratory Diseases

PRIMARY CARE - Patient presents with

acute or sub-acute asthma exacerbation

ASSESS the PATIENT - Is it asthma? Risk factor

for asthma related death? Severity of exacerbation

MILD OR MODER­

ATE Talks in phrases,

prefers sitting not

lying, not agitated.

Respiratory rate

increased Accessory

muscles not used

SEVERE Talks in words,

sits hunched forwards,

agitated Respiratory

rate >30/min Accessor...

📄 **Reference:** Page 402

### 4. STEP 1: Intermittent asthma

### STEP 1: Intermittent asthma

STEP 1: Intermittent asthma

~

Intermittent symptoms (< once/week)

HC3

~

Night time symptoms < twice/month

~

Normal physical activity...

📄 **Reference:** Page 403

### 5. Caution

### Caution

Caution

 Do not give medicines such as morphine, propranolol, or

other B-blockers to patients with asthma as they worsen

respiratory problems

 Do not give sedatives to children with asthma, even if they

are restless

339...

📄 **Reference:** Page 405


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 402, Page 403, Page 405

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 18. Query

> Chronic kidney disease staging referral

**Sources (top hits)**
- Page 516: Chronic Kidney Disease (CKD)
- Page 253: 3.1.1 Clinical Features of HIV
- Page 382: Risk Factor
- Page 1120: Surgery, Radiology and Anaesthesia
- Page 10: 7.1 Renal Diseases........................................................................448

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Chronic kidney disease staging referral

### 1. Chronic Kidney Disease (CKD)

### Chronic Kidney Disease (CKD)

7.1.2

Chronic Kidney Disease (CKD)      ICD10 CODE: N18

Chronic impairment of kidney function...

📄 **Reference:** Page 516

### 2. 3.1.1 Clinical Features of HIV

### 3.1.1 Clinical Features of HIV

3.1.1 Clinical Features of HIV

The WHO Clinical Staging of HIV for adults and children in the tables

below shows the typical clinical features of HIV infection. The staging is

based on demonstration of one or more opportunistic infections or key

findings and correlates with disease progression and prognosis. Clinical

staging should be performed at HIV diagnosis, on entry into HIV care,

at ART initiation and at every visit hereafter to help guide patient ...

📄 **Reference:** Page 253

### 3. Risk Factor

### Risk Factor

Risk Factor

Heart failure

Post myocardial infarction

Angina

Diabetes

Mild/moderate kidney disease

Advanced chronic kidney disease

Stroke

Carvedilol or Bisoprolol  only...

📄 **Reference:** Page 382

### 4. Surgery, Radiology and Anaesthesia

### Surgery, Radiology and Anaesthesia

Uganda Clinical Guidelines 2023

CHAPTER 24 : Surgery, Radiology and Anaesthesia

~

Hepatomegaly or cirrhosis (fibrotic

~

Gut perforation: Free air below the

~

Kidney diseases (cancer, chronic

hemidiaphgram on the CXR indi­

~

Liver/spleen rupture/ haematoma

pyelonephritis, hydronephrosis)

Ultrasound

~

Fluids (blood) in peritoneum

~

Renal trauma/haematoma

cate pneumoperitoneum

disease

Ultrasound

~

Gallstones, cholecystitis

~

Liver masse...

📄 **Reference:** Page 1120

### 5. 7.1 Renal Diseases........................................................................448

### 7.1 Renal Diseases........................................................................448

7.1 Renal Diseases........................................................................448

7.1.1 Acute Renal Failure........................................................................................448

7.1.2 Chronic Kidney Disease (CKD)........................................................................450

7.1.3 Use of Drugs in Renal Failure.............................................

📄 **Reference:** Page 10


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 10, Page 253, Page 382, Page 516, Page 1120

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 19. Query

> Exclusive breastfeeding six months

**Sources (top hits)**
- Page 317: Counselling on infant feeding choice
- Page 317: If mother chooses breastfeeding
- Page 953: 19.1.1  Infant and Young Child Feeding (IYCF)
- Page 825: If breastfeeding difficult:
- Page 920: HC2

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Exclusive breastfeeding six months

### 1. Counselling on infant feeding choice

### Counselling on infant feeding choice

Counselling on infant feeding choice

- Explain the risks of HIV transmission by breastfeeding (15%)

and other risks of not breastfeeding (malnutrition, diarrhoea)

- Mixed feeding may also increase risk of HIV transmission

- and diarrhoea

- Tell her about options for feeding, advantages, and risks

- Help her to assess choices, decide on the best option, and

then support her choice

- Feeding options

- Recommended

option:

Exclusive

breastfeeding...

📄 **Reference:** Page 317

### 2. If mother chooses breastfeeding

### If mother chooses breastfeeding

If mother chooses breastfeeding

- The risk may be reduced by keeping the breasts healthy

(mastitis and cracked nipples raise HIV infection risk)

- Advise exclusive breastfeeding for 3-6 months

251...

📄 **Reference:** Page 317

### 3. 19.1.1  Infant and Young Child Feeding (IYCF)

### 19.1.1  Infant and Young Child Feeding (IYCF)

19.1.1  Infant and Young Child Feeding (IYCF)

1.	 Counsel and support all mothers to initiate breastfeeding within an

hour of delivery and exclusively breastfeed their infants for the first

six months of life, unless medically contraindicated.

2.	 Teach mother correct positioning and attachment for breastfeeding,

how to express and store breast milk hygienically, and how to feed

the child by a cup.

3.	 Counsel and support parents to intro...

📄 **Reference:** Page 953

### 4. If breastfeeding difficult:

### If breastfeeding difficult:

Support exclusive breast­

feeding

on demand, day and night,

whenever baby wants

If breastfeeding difficult:

Help mother to position and

attach the baby

If breastfeeding not possible:

Advise on safe replacement feed­

ing (AFASS)

759...

📄 **Reference:** Page 825

### 5. HC2

### HC2

HC2

Routine deworming

every six months...

📄 **Reference:** Page 920


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 317, Page 825, Page 920, Page 953

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 20. Query

> Pre-eclampsia severe features magnesium sulfate

**Sources (top hits)**
- Page 795: Clinical features of severe pre-eclampsia
- Page 795: 16.3.7      Pre-Eclampsia
- Page 835: Obstetric Conditions
- Page 797: Mild to moderate pre-eclampsia
- Page 835: Blood pressure

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Pre-eclampsia severe features magnesium sulfate

### 1. Clinical features of severe pre-eclampsia

### Clinical features of severe pre-eclampsia

Clinical features of severe pre-eclampsia



Headache, blurring of vision of new onset



Epigastric or right upper quadrant pain, vomiting

729...

📄 **Reference:** Page 795

### 2. 16.3.7      Pre-Eclampsia

### 16.3.7      Pre-Eclampsia

16.3.7      Pre-Eclampsia	                     ICD10 CODE: O14

Pre-eclampsia is a hypertensive condition of pregnancy usually diag­

nosed after 20 weeks of gestation and can present as late as 4-6 weeks

postpartum.

It is haracterized with hypertension, proteinuria with or without oedema

and, may result into maternal fits if not managed appropriately.

It may also be superimposed on chronic hypertension. It is classified as

mild to severe pre-eclampsia.

TYPE ...

📄 **Reference:** Page 795

### 3. Obstetric Conditions

### Obstetric Conditions

Uganda Clinical Guidelines 2023

CHAPTER 16: Obstetric Conditions

as in non-pregnant women (see)



If no pre-eclampsia, give/contin­

ue appropriate antihypertensive

Severe Hypertension



Assess and treat for pre-eclamp­

sive as in non-pregnant women

tinue appropriate antihyperten­



If not pre-eclampsia, give/con­

sia (section 16.3.7). Refer to

tension



Assess for pre-eclampsia

Normal



No additional treatment



Review in one week

(section 4.1.6)

...

📄 **Reference:** Page 835

### 4. Mild to moderate pre-eclampsia

### Mild to moderate pre-eclampsia

Mild to moderate pre-eclampsia



Based on BP response



Methyldopa, oral, 250 mg every 8 hours as a starting

dose, increase to 500 mg 6 hourly according to response,

Max dose 2 g daily

AND/OR

HC3



Nifedipine 20-40 mg every 12 hours

Severe pre-eclampsia (hypertensive emergency)

To prevent convulsions

HC3



Give IV fluids (Normal saline) very slowly (1 L in 6-8

hours max)



Give IV loading dose of magnesium sulphate injection

(4 g of MgSO4)

...

📄 **Reference:** Page 797

### 5. Blood pressure

### Blood pressure

Blood pressure



History of

eclampsia

or pre-ec­

an hour

lampsia

769...

📄 **Reference:** Page 835


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 795, Page 797, Page 835

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 21. Query

> Sepsis empirical antibiotics adults

**Sources (top hits)**
- Page 792: Newborn
- Page 701: Medicines
- Page 785: Post-abortal Sepsis
- Page 792: 16.3.6       Antepartum Haemorrhage (APH) – Abruptio Placentae
- Page 792: If the woman has a Caesarean section

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Sepsis empirical antibiotics adults

### 1. Newborn

### Newborn

Newborn

H



Examine the neonate for suspected sepsis before

discharge



If newborn sepsis is suspected manage as in section

2.1.7.1



Advise the mother on how to recognize danger signs

(see section 17.1.1)...

📄 **Reference:** Page 792

### 2. Medicines

### Medicines

Medicines



Give antibiotics if there is evidence of surrounding cellulitis (see

section 22.1.3)



Control pain



Control odour with topical metronidazole



powder or gel until there is no foul smell



If patient has sepsis, give parenteral antibiotics (see section 2.1.7

for treatment of sepsis)...

📄 **Reference:** Page 701

### 3. Post-abortal Sepsis

### Post-abortal Sepsis

Post-abortal Sepsis

Patient has signs and symptoms

of sepsis following an abortion,

but there are no products of

conception in the uterus



Give IV antibiotics cef­

triaxone 2 g + metroni­

dazole 500



mg IV 8 hourly for

48 hours, until fever

has disappeared, then

switch to oral treatment

as for septic abortion

HC4



Refer to hospital for

evacuation...

📄 **Reference:** Page 785

### 4. 16.3.6       Antepartum Haemorrhage (APH) – Abruptio Placentae

### 16.3.6       Antepartum Haemorrhage (APH) – Abruptio Placentae

16.3.6       Antepartum Haemorrhage (APH) – Abruptio Placentae...

📄 **Reference:** Page 792

### 5. If the woman has a Caesarean section

### If the woman has a Caesarean section

If the woman has a Caesarean section



Continue the above antibiotics, and add metronidazole

500 mg IV every 8 hours

-

Continue until 48 hours after fever has gone...

📄 **Reference:** Page 792


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 701, Page 785, Page 792

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 22. Query

> Rabies post-exposure prophylaxis dog bite

**Sources (top hits)**
- Page 102: 1.2.1.4  Rabies Post Exposure Prophylaxis
- Page 4: 1.2 Trauma and Injuries..................................................................26
- Page 205: Caution: the patient may bite
- Page 204: 2.3.5 Rabies
- Page 102: Unit, Community Health Dept, Ministry of Health, September 2001

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Rabies post-exposure prophylaxis dog bite

### 1. 1.2.1.4  Rabies Post Exposure Prophylaxis

### 1.2.1.4  Rabies Post Exposure Prophylaxis

1.2.1.4  Rabies Post Exposure Prophylaxis           ICD10 CODE:

Z20.3, Z23...

📄 **Reference:** Page 102

### 2. 1.2 Trauma and Injuries..................................................................26

### 1.2 Trauma and Injuries..................................................................26

1.2 Trauma and Injuries..................................................................26

1.2.1 Bites and Stings..............................................................................................26

1.2.1.1  Snakebites.........................................................................................28

1.2.1.2 Insect Bites & Stings....................................................

📄 **Reference:** Page 4

### 3. Caution: the patient may bite

### Caution: the patient may bite

Caution: the patient may bite



Counsel caregivers on rabies and consequences

139...

📄 **Reference:** Page 205

### 4. 2.3.5 Rabies

### 2.3.5 Rabies

2.3.5 Rabies

ICD10 CODE: A82

Rabies is a viral infection of wild and domestic animals, transmitted to

humans by saliva of infected animals through bites, scratches or licks

on broken skin or mucuos membranes. Once symptoms develop, rabies

presents as a fatal encephalitis: there is no cure and treatment is palliative.

Before symptomatic disease has developed, rabies can effectively be

prevented by post-exposure prophylaxis....

📄 **Reference:** Page 204

### 5. Unit, Community Health Dept, Ministry of Health, September 2001

### Unit, Community Health Dept, Ministry of Health, September 2001

Post exposure prophylaxis effectively prevents the development of rabies

after the contact with saliva of infected animals, through bites, scratches,

licks on broken skin or mucous membranes. For further details refer to

Rabies Post-Exposure Treatment Guidelines, Veterinary Public Health

Unit, Community Health Dept, Ministry of Health, September 2001...

📄 **Reference:** Page 102


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 4, Page 102, Page 204, Page 205

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 23. Query

> Burns initial wound care and referral

**Sources (top hits)**
- Page 112: 2nd Degree burns or Partial thickness burns
- Page 112: Emergencies and Trauma
- Page 112: 4th Degree burns
- Page 116: Severe burns
- Page 115: At health facility

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Burns initial wound care and referral

### 1. 2nd Degree burns or Partial thickness burns

### 2nd Degree burns or Partial thickness burns

2nd Degree burns or Partial thickness burns

It is a dermal injury that is sub-classified as

superficial and deep 2nd degree burns. In su­

perficial 2nd degree burns, blisters result, the

pink moist wound is painful. A thin eschar is

formed. Heals in 10-14 days.

In deep 2nd degree burns, blisters are lacking,

the wound is pale, moderately painful, a thick

escar is formed. Heals in

>1 month, requiring surgical debridement...

📄 **Reference:** Page 112

### 2. Emergencies and Trauma

### Emergencies and Trauma

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma

CRITERIA

LEVEL...

📄 **Reference:** Page 112

### 3. 4th Degree burns

### 4th Degree burns

3rd Degree burns

Full thickness skin destruction, leather- like

rigid eschar. Painless on palpation or pinprick.

Requires skin graft.

4th Degree burns

Full thickness skin and fascia, muscles, or bone

destruction. Lifeless body part

Percentage of total

body surface area

(TBSA)

Small areas are estimated using the open palm

of the patient to represent 1% TBSA. Large

areas estimated using the “rules of nines” or

a Lund-Browder chart. Count all areas except

the one...

📄 **Reference:** Page 112

### 4. Severe burns

### Severe burns

Severe burns



First aid and wound management as above PLUS



Give IV fluid replacement in a total volume per 24 hours

according to the calculation in the box below (use crystal­

loids, i.e., Ringer’s lactate, or normal saline)



If patient in shock, run the IV fluids fast until BP improves

(see section 1.1.2)

HC4



Manage pain as necessary



Refer for admission



Monitor vital signs and urine output



Use antibiotics if there are systemic signs of infection:
...

📄 **Reference:** Page 116

### 5. At health facility

### At health facility

At health facility

HC2



Give oral or IV analgesics as required



If TBSA <10% and patient able to drink, give oral fluids

otherwise consider IV



Give TT if not fully immunised



Leave small blisters alone, drain large blisters and dress

if closed dressing method is being used the urine output.

The normal urine output is: Children (<30 kg) 1-2 ml/kg/

hour and adults 0.5 ml/kg/hour (30-50 ml /hour)



Dress with silver sulphadiazine cream 1%, add saline

moi...

📄 **Reference:** Page 115


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 112, Page 115, Page 116

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 24. Query

> Snake bite envenomation hospital referral

**Sources (top hits)**
- Page 96: without envenomation
- Page 96: Management
- Page 96: Emergencies and Trauma
- Page 96: If local necrosis develops
- Page 96: If signs of fang penetration

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Snake bite envenomation hospital referral

### 1. without envenomation

### without envenomation

If no signs and symptoms for 6-8 hours: most likely bite

without envenomation

~

Observation for 12-24 hours recommended

~

Tetanus toxoid (TT) IM 0.5 ml if not previously

immunised in the last 10 years...

📄 **Reference:** Page 96

### 2. Management

### Management

Management

What to do

What not to do

 Do not panic

 Reassure the patient to

 Do not lay the patient on

stay calm

 Lay the patient on the

their back as it may block

airways

 Do not apply a tourniquet

side to avoid movement

of affected areas

 Remove all tight items

 Do not squeeze or incise the

wound

 Do not attempt to suck the

around the affected area

 Leave the wound/bite

venom out

 Do not try to kill or attack

area alone

 Immobilize the patient

...

📄 **Reference:** Page 96

### 3. Emergencies and Trauma

### Emergencies and Trauma

Uganda Clinical Guidelines 2023

CHAPTER 1: Emergencies and Trauma...

📄 **Reference:** Page 96

### 4. If local necrosis develops

### If local necrosis develops

If local necrosis develops

~

Remove blisters, clean and dress daily, debride

after lesions stabilise (minimum 15 days)

30...

📄 **Reference:** Page 96

### 5. If signs of fang penetration

### If signs of fang penetration

If signs of fang penetration

~

Immobilise limb with a splint

~

Analgesic e.g. paracetamol (avoid NSAIDS like

aspirin, diclofenac, ibuprofen)...

📄 **Reference:** Page 96


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 96

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 25. Query

> Neonatal sepsis danger signs referral

**Sources (top hits)**
- Page 792: Newborn
- Page 153: Causes
- Page 183: 2.1.7.1 Neonatal Septicaemia
- Page 863: If danger signs present, treat as below
- Page 892: 17.3.21   Check for General Danger Signs

**Response**

```
**Uganda Clinical Guidelines 2023**

**Question:** Neonatal sepsis danger signs referral

### 1. Newborn

### Newborn

Newborn

H



Examine the neonate for suspected sepsis before

discharge



If newborn sepsis is suspected manage as in section

2.1.7.1



Advise the mother on how to recognize danger signs

(see section 17.1.1)...

📄 **Reference:** Page 792

### 2. Causes

### Causes

Causes

~

Surgical causes.

- Head Injury, Chest trauma

~

Medical Causes

- Severe Asthma, Pneumonia, Sepsis, Shock, Malaria,

Covid-19, Heart Failure, Cardiac arrest, Upper airway

obstruction, Severe anaemia, Pertussis, Carbon Monoxide

poisoning.

~

Obstetric, gynaecological, and perioperative causes.

- Obstructed labour, Ruptured uterus, Pre-eclampsia and

eclampsia, Post caesarean section,

~

Neonatal causes

- Transient tachypnoea of the new-born, Hypoxic Ischaemic

encep...

📄 **Reference:** Page 153

### 3. 2.1.7.1 Neonatal Septicaemia

### 2.1.7.1 Neonatal Septicaemia

2.1.7.1 Neonatal Septicaemia

Organisms causing neonatal septicemia are similar to the ones causing

neonatal pneumonia and meningitis. Refer to hospital after pre-referral

dose of antibiotics....

📄 **Reference:** Page 183

### 4. If danger signs present, treat as below

### If danger signs present, treat as below

If danger signs present, treat as below

pustules and apply Gentian



If referral not possible continue

every 12 hours plus gentamicin

gentamicin 5-7 mg/Kg every



Give ampicillin 50 mg/kg IM



Clean infected umbilicus and

Kg IV/IM every 6 hours and

5 mg/kg every 24 hours (4

tion, give cloxacillin 50 mg/



If risk of staphylococcus infec­



Refer baby to hospital

treatment for 7 days

mg/kg if preterm)



Keep baby warm

24 hours

Vio...

📄 **Reference:** Page 863

### 5. 17.3.21   Check for General Danger Signs

### 17.3.21   Check for General Danger Signs

17.3.21   Check for General Danger Signs...

📄 **Reference:** Page 892


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 153, Page 183, Page 792, Page 863, Page 892

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---
