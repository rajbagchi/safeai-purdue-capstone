# WHO Malaria pipeline run report

- **Generated (UTC)**: 2026-03-19T23:56:20.427900+00:00
- **Preset**: who-malaria (NIH Bookshelf)
- **PDF**: `C:\temp\capstone\Bookshelf_NBK588130.pdf`
- **KB output directory**: `C:\temp\capstone\medical_kb_who_malaria`
- **Reuse KB flag**: `False`

---
## Stage 1: Multi-pass extraction

| Metric | Value |
|--------|-------|
| PDF path | `C:\temp\capstone\Bookshelf_NBK588130.pdf` |
| Extraction timestamp | 2026-03-19T18:56:03.587250 |
| Total pages extracted | 478 |
| Tables extracted | 200 |
| Embedded images saved | 2 |
| OCR / manual-review flags | 0 |
| Cross-validation method | pdfplumber |
| Cross-validation consistency score | 0.8272014394238952 |
| Passes logged | 5 |

### Extraction passes

| Pass | Strategy | Details |
|------|----------|---------|
| 0 | `analysis` | `{"pass": 0, "strategy": "analysis", "profile_pages_sample": "[{'page': 1, 'text_length': 0, 'has_images': False, 'has_vector_graphics': True}"}` |
| 1 | `text_extraction` | `{"pass": 1, "strategy": "text_extraction", "pages": 478}` |
| 2 | `table_extraction` | `{"pass": 2, "strategy": "table_extraction", "tables_found": 200}` |
| 4 | `cross_validation` | `{"pass": 4, "strategy": "cross_validation", "results": {"method": "pdfplumber", "page_matches": [{"page": 2, "similarity": 0.9791284403669723}, {"page": 3, "similarity": 0.983258352385869}, {"page": 4, "similarity": 0.9833528722157092}, {"p` |
| images | `embedded_raster` | `{"pass": "images", "strategy": "embedded_raster", "images_saved": 2}` |

## Stage 2: Validation

### Overall

- **Passed (threshold)**: False
- **Confidence**: 70.54%
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
    "pages_extracted": 478
  }
}
```

### Tables

```json
{
  "stage": "tables",
  "passed": true,
  "issues": [],
  "confidence": 1.0,
  "suggestions": [],
  "metadata": {
    "tables_extracted": 200,
    "valid_tables": 200
  }
}
```

### Cross

```json
{
  "stage": "cross_consistency",
  "passed": false,
  "issues": [
    "Low cross-validation consistency: 82.7%"
  ],
  "confidence": 0.8272014394238952,
  "suggestions": [
    "Review pages with low consistency scores"
  ],
  "metadata": {
    "consistency_score": 0.8272014394238952
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
      "contraindication",
      "warning",
      "severe malaria",
      "artemisinin",
      "pregnancy",
      "children",
      "infant",
      "emergency"
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
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy",
    "Safety-critical information - verify accuracy"
  ],
  "confidence": 0.0,
  "suggestions": [
    "Prioritize flagged items for manual review"
  ],
  "metadata": {
    "items_for_review": [
      {
        "type": "dosing_table",
        "page": 28,
        "reason": "Dosing accuracy critical - requires human verification"
      },
      {
        "type": "dosing_table",
        "page": 29,
        "reason": "Dosing accuracy critical - requires human verification"
      },
      {
        "type": "dosing_table",
        "page": 173,
        "reason": "Dosing accuracy critical - requires human verification"
      },
      {
        "type": "dosing_table",
        "page": 174,
        "reason": "Dosing accuracy critical - requires human verification"
      },
      {
        "type": "dosing_table",
        "page": 175,
        "reason": "Dosing accuracy critical - requires human verification"
      },
      {
        "type": "dosing_table",
        "page": 175,
        "reason": "Dosing accuracy critical - requires human verification"
      },
      {
        "type": "dosing_table",
        "page": 176,
        "reason": "Dosing accuracy critical - requires human verification"
      },
      {
        "type": "dosing_table",
        "page": 178,
        "reason": "Dosing accuracy critical - requir
... (truncated)
```

## Stage 3: Chunking + BM25 index

| Metric | Value |
|--------|-------|
| Total chunks | 5534 |
| Chunks with tables | 4738 |

### Sample chunk headings (first 15)

- p.2 — **WHO guidelines for malaria - 13 August 2025**
- p.2 — **Contact**
- p.2 — **Sponsors/Funding**
- p.2 — **Disclaimer**
- p.2 — **2025**
- p.2 — **Suggested citation**
- p.2 — **Cataloguing-in-Publication (CIP) data.**
- p.2 — **Sales, rights and licensing.**
- p.2 — **Third-party materials.**
- p.2 — **isclaimers.**
- p.3 — **Sections**
- p.4 — **Untitled**
- p.5 — **Pyrethroid-only nets (2019)**
- p.5 — **Pyrethroid-PBO ITNs (2022)**
- p.6 — **Untitled**

## Stage 4: Guardrail brain

`MedicalGuardrailBrain` validates each composed answer: triage headings, dangerous patterns, citations vs. chunk pages.

## Stage 5: Search & Q&A (25 queries)

BM25 top-5 excerpts per query; guardrail summary below each.

### 1. Query

> What is the treatment for uncomplicated Plasmodium falciparum malaria?

**Sources (top hits)**
- Page 437: References
- Page 308: Untitled
- Page 435: References
- Page 190: knowlesi
- Page 310: Untitled

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** What is the treatment for uncomplicated Plasmodium falciparum malaria?

### 1. References

### References

References

219. Pryce J, Taylor M, Fox T, Hine P. Pyronaridine-artesunate for treating uncomplicated Plasmodium falciparum malaria.

Cochrane Database Syst Rev 2022;6(6) Pubmed Journal...

📄 **Reference:** Page 437

### 2. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

220. . The effect of dosing regimens on the antimalarial efficacy of dihydroartemisinin-piperaquine: a pooled analysis of individual patient

data. PLoS medicine 2013;10(12):e1001564; discussion e1001564 Pubmed Journal

221. Graves PM, Gelband H, Garner P. Primaquine or other 8-aminoquinoline for reducing P. falciparum transmission. The Cochrane

database of systematic reviews 2014;(6):CD008152 Pubmed Journal

222. Wh...

📄 **Reference:** Page 308

### 3. References

### References

References

219. Pryce J, Taylor M, Fox T, Hine P. Pyronaridine-artesunate for treating uncomplicated Plasmodium falciparum malaria.

Cochrane Database Syst Rev 2022;6(6) Pubmed Journal...

📄 **Reference:** Page 435

### 4. knowlesi

### knowlesi

5.2.1.5 Uncomplicated malaria caused by P. vivax, P. ovale, P. malariae or P.

knowlesi

Plasmodium vivax accounts for approximately half of all malaria cases outside Africa [3][250][251]. It is prevalent in the Middle

East, Asia, the Western Pacific and Central and South America. With the exception of the Horn, it is rarer in Africa, where there

is a high prevalence of the Duffy-negative phenotype, particularly in West Africa, although cases are reported in both

Mauritania and ...

📄 **Reference:** Page 190

### 5. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

in early infancy. Clinical infectious diseases : an official publication of the Infectious Diseases Society of America 2009;48(12):1704-12

Pubmed Journal

256. Genton B, D'Acremont V, Rare L, Baea K, Reeder JC, Alpers MP, et al. Plasmodium vivax and mixed infections are associated with

severe malaria in children: a prospective cohort study from Papua New Guinea. PLoS medicine 2008;5(6):e127 Pubmed Journal

257. Koch...

📄 **Reference:** Page 310


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 190, Page 308, Page 310, Page 435, Page 437

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 2. Query

> Dosing artemisinin-based combination therapy in children under 5

**Sources (top hits)**
- Page 226: Considerations in use of artemisinin-based combination therapy
- Page 443: Intervention:
- Page 443: h
- Page 443: High
- Page 443: High

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Dosing artemisinin-based combination therapy in children under 5

### 1. Considerations in use of artemisinin-based combination therapy

### Considerations in use of artemisinin-based combination therapy

Considerations in use of artemisinin-based combination therapy

Oral artemisinin and its derivatives (e.g. artesunate, artemether, dihydroartemisinin) should not be used alone. In order to simplify use,

improve adherence and minimize the availability of oral artemisinin monotherapy, fixed-dose combination ACTs are strongly preferred

to co-blistered or co-dispensed loose tablets and should be used when they are readily availabl...

📄 **Reference:** Page 226

### 2. Intervention:

### Intervention:

Intervention: Artemisinin-based combination therapy...

📄 **Reference:** Page 443

### 3. h

### h

h...

📄 **Reference:** Page 443

### 4. High

### High

High...

📄 **Reference:** Page 443

### 5. High

### High

High

1...

📄 **Reference:** Page 443


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 226, Page 443

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 3. Query

> Severe malaria definition and management

**Sources (top hits)**
- Page 403: Publication bias: no serious.
- Page 402: 167
- Page 404: Publication bias: no serious.
- Page 210: 5.2.2 Treating severe malaria
- Page 402: Intervention

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Severe malaria definition and management

### 1. Publication bias: no serious.

### Publication bias: no serious.

children, in the 12 months following administration of the first three doses, protective efficacy against clinical (uncomplicated and

severe) malaria was 51% (95% CI 47-55) (per protocol analysis).

3. [Impact outcome] Protective efficacy (%) against clinical malaria episodes (per protocol analysis) Clinical malaria assessed with:

illness in a child brought to a study facility with a measured temperature of 37.5°C and P. falciparum asexual parasitaemia at a d...

📄 **Reference:** Page 403

### 2. 167

### 167

based

vaccination) 167

month 46.

Pilot

implementation

study 2019–2023

6 Important

1. [Impact outcome] Protective efficacy (%) against clinical malaria episodes (modified intention-to-treat analysis). Per-protocol

analysis protective efficacy 39.0% (95% CI 34.3 to 43.3). Clinical malaria assessed with: illness in a child brought to a study facility

with a measured temperature of 37.5°C and P. falciparum asexual parasitaemia at a density of > 5000 parasites per cubic millimetre o...

📄 **Reference:** Page 402

### 3. Publication bias: no serious.

### Publication bias: no serious.

defined as radiographically proven pneumonia, meningitis established by analysis of cerebrospinal fluid, sepsis (with positive blood

culture), or gastroenteritis with severe dehydration). Laboratory tests and other examinations (chest x-ray, lumbar puncture, blood

culture) to exclude co-morbidities were performed only if there was a clinical suspicion/diagnosis justifying additional investigations.

The study included 450 total participants with three study a...

📄 **Reference:** Page 404

### 4. 5.2.2 Treating severe malaria

### 5.2.2 Treating severe malaria

5.2.2 Treating severe malaria

Mortality from untreated severe malaria (particularly cerebral malaria) approaches 100%. With prompt, effective antimalarial

treatment and supportive care, the rate falls to 10–20% overall. Within the broad definition of severe malaria some syndromes are

associated with lower mortality rates (e.g. severe anaemia) and others with higher mortality rates (e.g. acidosis). The risk for death

increases in the presence of multiple com...

📄 **Reference:** Page 210

### 5. Intervention

### Intervention

Outcome

Timeframe

Study results and

Intervention

Malaria vaccination...

📄 **Reference:** Page 402


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 210, Page 402, Page 403, Page 404

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 4. Query

> When to refer a patient with malaria to hospital?

**Sources (top hits)**
- Page 220: Follow-on treatment
- Page 128: Research needs
- Page 163: 4. Appropriate weight-based dosing
- Page 177: 5.2.1.2 Recurrent falciparum malaria
- Page 211: Follow-on treatment

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** When to refer a patient with malaria to hospital?

### 1. Follow-on treatment

### Follow-on treatment

Follow-on treatment

The current recommendation of experts is to give parenteral antimalarial drugs for the treatment of severe malaria for a

minimum of 24 h ounce started (irrespective of the patient’s ability to tolerate oral medication earlier) or until the patient can

tolerate oral medication, before giving the oral follow-up treatment.

After initial parenteral treatment, once the patient can tolerate oral therapy, it is essential to continue and complete treatmen...

📄 **Reference:** Page 220

### 2. Research needs

### Research needs

Research needs

The GDG identified the following evidence gaps as requiring further research. These relate to:

•

the optimal duration for PDMC in different geographical and transmission settings, and understanding of the short-, medium-

and long-term benefits of PDMC of different durations; these evaluations should recognize the underlying pattern of post-

discharge death and/or re-admission, and the higher risk of some groups dying soon after discharge; to minimize bias,...

📄 **Reference:** Page 128

### 3. 4. Appropriate weight-based dosing

### 4. Appropriate weight-based dosing

4. Appropriate weight-based dosing

To prolong their useful therapeutic life and ensure that all patients have an equal chance of being cured, the quality of antimalarial drugs

must be ensured, and antimalarial drugs must be given at optimal dosages. Treatment should maximize the likelihood of rapid clinical and

parasitological cure and minimize transmission from the treated infection. To achieve this, dosage regimens should be based on the

patient’s we...

📄 **Reference:** Page 163

### 4. 5.2.1.2 Recurrent falciparum malaria

### 5.2.1.2 Recurrent falciparum malaria

5.2.1.2 Recurrent falciparum malaria

Recurrence of P. falciparum malaria can result from re-infection or recrudescence (treatment failure). Treatment failure may

result from drug resistance or inadequate exposure to the drug due to sub-optimal dosing, poor adherence, vomiting, unusual

pharmacokinetics in an individual, or substandard medicines. It is important to determine from the patient’s history whether he

or she vomited the previous treatment or...

📄 **Reference:** Page 177

### 5. Follow-on treatment

### Follow-on treatment

Follow-on treatment

The current recommendation of experts is to give parenteral antimalarial drugs for the treatment of severe malaria for a minimum

of 24 h once started (irrespective of the patient’s ability to tolerate oral medication earlier) or until the patient can tolerate oral

medication, before giving the oral follow-up treatment.

After initial parenteral treatment, once the patient can tolerate oral therapy, it is essential to continue and complete treatment...

📄 **Reference:** Page 211


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 128, Page 163, Page 177, Page 211, Page 220

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 5. Query

> Pregnancy and malaria treatment recommendations

**Sources (top hits)**
- Page 185: Feasibility
- Page 302: Untitled
- Page 30: Scope
- Page 108: Implementation
- Page 184: Untitled

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Pregnancy and malaria treatment recommendations

### 1. Feasibility

### Feasibility

Feasibility

One consideration in determining the feasibility of the recommendation on treatment of malaria in

the first trimester is that the existing warning against the use of artemisinin in the first trimester

implies the need to consistently screen for pregnancy among all women of childbearing potential

prior to treatment for malaria. However, pregnancy screening is rarely done prior to initiating

malaria treatment. As observed by national programmes, the contraindicati...

📄 **Reference:** Page 185

### 2. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

temperature, and relative humidity: an experimental study in rural Gambia. The Lancet Planetary Health 2018;2(11):e498-e508 Pubmed

Journal Website

114. Norms, standards and processes underpinning development of WHO recommendations on vector control. Geneva: World Health

Organization 2020. Website

115. Sicuri E, Bardají A, Nhampossa T, Maixenchs M, Nhacolo A, Nhalungo D, et al. Cost-effectiveness of intermittent pr...

📄 **Reference:** Page 302

### 3. Scope

### Scope

Scope

The consolidated WHO Guidelines for malaria bring together all recommendations for malaria, including prevention using vector control,

preventive chemotherapy and the vaccine; diagnosis, treatment and elimination strategies. The Guidelines also provide links to other

resources including unpublished evidence reviewed at the time of formulating recommendations, guidance and information on strategic

use of information to drive impact, surveillance, monitoring and evaluation, op...

📄 **Reference:** Page 30

### 4. Implementation

### Implementation

Implementation

Please refer to the WHO policy brief for the implementation of intermittent preventive treatment of malaria in pregnancy using

sulfadoxine-pyrimethamine (IPTp-SP) [128] and the WHO recommendations on antenatal care for a positive pregnancy

experience [130]. A field guide on community deployment of intermittent preventive treatment of malaria in pregnancy with

sulfadoxine-pyrimethamine was released in January 2024 [129]. A manual for subnational tailoring of...

📄 **Reference:** Page 108

### 5. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

based therapies, and in how different cultures would value the outcomes being monitored, such

as perceptions around early trimester pregnancy losses, low birthweight and anaemia. However,

artemether-lumefantrine compared to quinine is likely to be a more attractive option because of its

greater availability and the convenience of a shorter, better tolerated treatment. Policy-makers and

implementers will obviously ...

📄 **Reference:** Page 184


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 30, Page 108, Page 184, Page 185, Page 302

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 6. Query

> Drug interactions with artemether lumefantrine

**Sources (top hits)**
- Page 184: Untitled
- Page 185: Acceptability
- Page 118: Antimalarial medicine
- Page 173: Remarks
- Page 173: 5.2.1.1.2 Dosing of ACTs

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Drug interactions with artemether lumefantrine

### 1. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

based therapies, and in how different cultures would value the outcomes being monitored, such

as perceptions around early trimester pregnancy losses, low birthweight and anaemia. However,

artemether-lumefantrine compared to quinine is likely to be a more attractive option because of its

greater availability and the convenience of a shorter, better tolerated treatment. Policy-makers and

implementers will obviously ...

📄 **Reference:** Page 184

### 2. Acceptability

### Acceptability

Acceptability

In considering the acceptability of artemether-lumefantrine versus quinine treatments, the GDG

looked to how quinine is presently being used and accepted.

Adherence to quinine is low because it is frequently associated with adverse effects, including

cinchonism, nausea and hypoglycaemia [231][243][244]. In a review of 35 national guidelines,

66% recommended oral quinine as first-line treatment for uncomplicated malaria in the first

trimester of pregnancy. O...

📄 **Reference:** Page 185

### 3. Antimalarial medicine

### Antimalarial medicine

Antimalarial medicine

Drug regimens evaluated for IPTsc and found to be effective include SP combined with an aminoquinoline (either AQ or

piperaquine), SP+AS, and artemisinin-based combination therapy including an aminoquinoline (AS-AQ or DHAP)1. SP+AQ has

been widely used for chemoprevention in West Africa and has been shown to be efficacious, safe, well tolerated, available and

inexpensive. In order to reduce the risk of drug resistance to life-saving drugs, fir...

📄 **Reference:** Page 118

### 4. Remarks

### Remarks

Remarks

Longer ACT treatment may be required to achieve > 90% cure rate in areas with artemisinin-resistant P. falciparum, but

there are insufficient trials to make definitive recommendations. A 3-day course of the artemisinin component of ACTs

covers two asexual cycles, ensuring that only a small fraction of parasites remain for clearance by the partner drug, thus

reducing the potential development of resistance to the partner drug. Shorter courses (1–2 days) are therefore not
...

📄 **Reference:** Page 173

### 5. 5.2.1.1.2 Dosing of ACTs

### 5.2.1.1.2 Dosing of ACTs

5.2.1.1.2 Dosing of ACTs

ACT regimens must ensure optimal dosing to prolong their useful therapeutic life, i.e. to maximize the likelihood of rapid

clinical and parasitological cure, minimize transmission and retard drug resistance.

It is essential to achieve effective antimalarial drug concentrations for a sufficient time (exposure) in all target populations in

order to ensure high cure rates. The dosage recommendations below are derived from understanding the ...

📄 **Reference:** Page 173


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 118, Page 173, Page 184, Page 185

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 7. Query

> Prophylaxis for travelers to endemic areas

**Sources (top hits)**
- Page 453: Moderate
- Page 453: Moderate
- Page 453: Untitled
- Page 453: Intervention:
- Page 453: Population:

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Prophylaxis for travelers to endemic areas

### 1. Moderate

### Moderate

Moderate

Due to serious...

📄 **Reference:** Page 453

### 2. Moderate

### Moderate

Moderate

Due to serious...

📄 **Reference:** Page 453

### 3. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)...

📄 **Reference:** Page 453

### 4. Intervention:

### Intervention:

Intervention: Chloroquine prophylaxis...

📄 **Reference:** Page 453

### 5. Population:

### Population:

Population: Malaria-endemic areas...

📄 **Reference:** Page 453


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 453

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 8. Query

> Rapid diagnostic test interpretation false positives

**Sources (top hits)**
- Page 267: Untitled
- Page 307: Untitled
- Page 447: Target conditions
- Page 447: Untitled
- Page 447: Summary

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Rapid diagnostic test interpretation false positives

### 1. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

chemotherapy

prophylaxis

Any method of protection from or prevention of disease; when applied to chemotherapy, it is commonly

termed “chemoprophylaxis”.

prophylaxis, causal

Complete prevention of erythrocytic infection by destroying the pre-erythrocytic forms of the parasite

rapid diagnostic test

(RDT)

Immunochromatographic lateral flow device for rapid detection of malaria parasite antigens

rapid diagnostic ...

📄 **Reference:** Page 267

### 2. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

200. Malaria diagnosis: memorandum from a WHO meeting. Bulletin of the World Health Organization 1988;66(5):575-94 Pubmed

201. Malaria microscopy quality assurance manual, version 2. Geneva: World Health Organization 2016. Website

202. Kawamoto F, Billingsley PF. Rapid diagnosis of malaria by fluorescence microscopy. Parasitology today (Personal ed.)

1992;8(2):69-71 Pubmed

203. Malaria diagnosis: new perspectives....

📄 **Reference:** Page 307

### 3. Target conditions

### Target conditions

•

Patients with malaria who undergoing G6PD testing to inform treatment with primaquine or tafenoquine to prevent

relapses of P. vivax and P. ovale.

•

Index test is semi-quantitative near-patient tests for G6PD.

•

Reference standard is the quality assured G6PD spectrophotometric assay using the adjusted male median (AMM) as

the standardised metric of 100% G6PD activity. For the Standard G6PD biosensor used with the STANDARD G6PD

Analyzer (SB Biosensor, Inc) a suppl...

📄 **Reference:** Page 447

### 4. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

Qualitative FST and (d) consists of 753 participants assessed by CareStart G6PD enrolled in the Lao People’s Democratic Republic. Henriques 2018 (a) and

(c) were chosen, due to having a more complete sample size.

Bancone 2015(a)excluded from meta-analysis, because Bancone 2015 (a) and (b) use the same participants. Difference between two studies are

that(a) uses capillary blood and (b) uses venous blood samples. Ba...

📄 **Reference:** Page 447

### 5. Summary

### Summary

Summary...

📄 **Reference:** Page 447


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 267, Page 307, Page 447

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 9. Query

> G6PD deficiency and primaquine

**Sources (top hits)**
- Page 208: Primaquine and glucose-6-phosphate dehydrogenase deficiency
- Page 195: Practical info
- Page 199: Untitled
- Page 208: Benefits and harms
- Page 195: Qualitative near-patient G6PD tests (2024)

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** G6PD deficiency and primaquine

### 1. Primaquine and glucose-6-phosphate dehydrogenase deficiency

### Primaquine and glucose-6-phosphate dehydrogenase deficiency

Primaquine and glucose-6-phosphate dehydrogenase deficiency

Any person (male or female) with red cell G6PD activity < 30% of the normal mean has G6PD deficiency and will experience

haemolysis after primaquine. Heterozygote females with higher mean red cell activities may still show substantial haemolysis.

G6PD deficiency is an inherited sex-linked genetic disorder, which is associated with some protection against P. falciparum

...

📄 **Reference:** Page 208

### 2. Practical info

### Practical info

Practical info

Please refer to Testing for G6PD deficiency for safe use of primaquine in radical cure of P. vivax and P. ovale (Policy

brief) [264] and Guide to G6PD deficiency rapid diagnostic testing to support P. vivax radical cure [265].

If G6PD testing is not available, a decision to prescribe or withhold primaquine should be based on the balance of the

probability and benefits of preventing relapse against the risks of primaquine-induced haemolytic anaemia. This dep...

📄 **Reference:** Page 195

### 3. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

In order to prevent relapses of P. vivax and P. ovale, and when the G6PD status of the patient was previously unknown, the

following recommendations are made:

A. If only a qualitative near-patient test for G6PD deficiency is available, tafenoquine single dose treatment or high

dose primaquine (1mg/kg/day for 7 days) should not be given. If by the qualitative test the patient is classified as non-

deficient primaqu...

📄 **Reference:** Page 199

### 4. Benefits and harms

### Benefits and harms

Benefits and harms

Desirable effects:

•

There are no comparative trials of the efficacy or safety of primaquine in people with G6PD

deficiency.

Undesirable effects:

•

Primaquine is known to cause haemolysis in people with G6PD deficiency.

•

Of the 15 trials included in the systematic review, 12 explicitly excluded people with G6PD

deficiency; in three trials, it was unclear whether participants were tested for G6PD deficiency or

excluded. None of the trials rep...

📄 **Reference:** Page 208

### 5. Qualitative near-patient G6PD tests (2024)

### Qualitative near-patient G6PD tests (2024)

Qualitative near-patient G6PD tests (2024)

Qualitative near-patient tests for G6PD deficiency should be used to inform administration of specific treatment regimens to

prevent relapses of P. vivax and P. ovale. G6PD non-deficient individuals can receive 0.5 mg/kg/day primaquine for 14 days or

0.5 mg/kg/day primaquine for 7 days.

•

In males and females, <30% of normal G6PD activity is considered deficient.

•

In patients undergoing G6PD activi...

📄 **Reference:** Page 195


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 195, Page 199, Page 208

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 10. Query

> Malaria vaccine recommendations RTS,S R21

**Sources (top hits)**
- Page 159: Certainty of the evidence related to the safety of R21/Matrix-M
- Page 386: Systematic review summary
- Page 162: immunization systems.
- Page 386: RTS,S/AS01 vs
- Page 386: Summary

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Malaria vaccine recommendations RTS,S R21

### 1. Certainty of the evidence related to the safety of R21/Matrix-M

### Certainty of the evidence related to the safety of R21/Matrix-M

Certainty of the evidence related to the safety of R21/Matrix-M ranged from LOW to MODERATE due to

few or no events, wide CIs and small sample size. While the vaccine was associated with febrile seizures at

a rate of approximately one per 2500 vaccinations, all febrile seizures resolved without sequelae. There was

no imbalance in other severe adverse events (SAEs) among children vaccinated with R21/Matrix-M or with

the cont...

📄 **Reference:** Page 159

### 2. Systematic review summary

### Systematic review summary

Systematic review summary

Six studies form the basis of these recommendations: five were individual randomized controlled trials (RCTs) and one was an open-

label extension study of an included RCT. One RCT was a multicentre study evaluating three or four doses of the RTS,S/AS01 malaria

vaccine compared to no malaria vaccination. One RCT evaluated the seasonal administration of RTS,S/AS01 malaria vaccine alone

compared to SMC alone, and also compared a combinat...

📄 **Reference:** Page 386

### 3. immunization systems.

### immunization systems.

Feasibility

Malaria vaccine introduction is feasible with good and equitable coverage, as seen through routine

immunization systems.

Administrative data from early implementing areas through 46 months of RTS,S/AS01 vaccinations under the

pilot programme showed the following:

•

About 4.2 million RTS,S/AS01 vaccine doses were administered across the three pilot countries and

more than 1.2 million children received their first dose.

•

All three countries reached ...

📄 **Reference:** Page 162

### 4. RTS,S/AS01 vs

### RTS,S/AS01 vs

RTS,S/AS01 vs...

📄 **Reference:** Page 386

### 5. Summary

### Summary

Summary...

📄 **Reference:** Page 386


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 159, Page 162, Page 386

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 11. Query

> Resistance to artemisinin in Southeast Asia

**Sources (top hits)**
- Page 226: Untitled
- Page 222: Artemisinin-resistant falciparum malaria
- Page 226: Considerations in use of artemisinin-based combination therapy
- Page 191: P. vivax
- Page 192: P. vivax

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Resistance to artemisinin in Southeast Asia

### 1. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

for days or weeks after effective treatment. HRP2-detecting RDTs are not suitable for detecting treatment failure. RDTs are slightly less

sensitive for detecting P. malariae and P. ovale. The WHO Malaria RDT Product Testing programme provides comparative data on the

performance of RDT products to guide procurement. Since 2008, 210 products have been evaluated in five rounds of product

testing [207].

For the diagno...

📄 **Reference:** Page 226

### 2. Artemisinin-resistant falciparum malaria

### Artemisinin-resistant falciparum malaria

Artemisinin-resistant falciparum malaria

Artemisinin resistance in P. falciparum is now prevalent in parts of Cambodia, the Lao People’s Democratic Republic,

Myanmar, Thailand and Viet Nam. There is currently no evidence for artemisinin resistance outside these areas. The particular

advantage of artemisinins over other antimalarial drugs is that they kill circulating ring-stage parasites and thus accelerate

therapeutic responses. This is lost in ...

📄 **Reference:** Page 222

### 3. Considerations in use of artemisinin-based combination therapy

### Considerations in use of artemisinin-based combination therapy

Considerations in use of artemisinin-based combination therapy

Oral artemisinin and its derivatives (e.g. artesunate, artemether, dihydroartemisinin) should not be used alone. In order to simplify use,

improve adherence and minimize the availability of oral artemisinin monotherapy, fixed-dose combination ACTs are strongly preferred

to co-blistered or co-dispensed loose tablets and should be used when they are readily availabl...

📄 **Reference:** Page 226

### 4. P. vivax

### P. vivax

In areas with chloroquine-sensitive P. vivax

For chloroquine-sensitive vivax malaria, oral chloroquine at a total dose of 25 mg base/kg bw is effective and well tolerated.

Lower total doses are not recommended, as these encourage the emergence of resistance. Chloroquine is given at an initial

dose of 10 mg base/kg bw, followed by 10 mg/kg bw on the second day and 5 mg/kg bw on the third day. In the past, the initial

10 mg/kg bw dose was followed by 5 mg/kg bw at 6 h, 24 h and 4...

📄 **Reference:** Page 191

### 5. P. vivax

### P. vivax

In areas with chloroquine-sensitive P. vivax

For chloroquine-sensitive vivax malaria, oral chloroquine at a total dose of 25 mg base/kg bw is effective and well tolerated.

Lower total doses are not recommended, as these encourage the emergence of resistance. Chloroquine is given at an initial

dose of 10 mg base/kg bw, followed by 10 mg/kg bw on the second day and 5 mg/kg bw on the third day. In the past, the initial

10-mg/kg bw dose was followed by 5 mg/kg bw at 6 h, 24 h and 4...

📄 **Reference:** Page 192


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 191, Page 192, Page 222, Page 226

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 12. Query

> Hypoglycemia in severe malaria

**Sources (top hits)**
- Page 268: Untitled
- Page 458: Population:
- Page 211: Treatment of severe malaria
- Page 386: Systematic review summary
- Page 157: Benefits and harms

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Hypoglycemia in severe malaria

### 1. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

severe anaemia

Haemoglobin concentration of < 5 g/100 mL (haematocrit < 15%)

severe falciparum

malaria

Acute falciparum malaria with signs of severe illness and/or evidence of vital organ dysfunction

single-dose regimen

Administration of a medicine as a single dose to achieve a therapeutic objective

slide positivity rate

Proportion of blood smears found to be positive for Plasmodium among all blood smears exam...

📄 **Reference:** Page 268

### 2. Population:

### Population:

Population: Children with severe malaria (malaria-endemic countries)...

📄 **Reference:** Page 458

### 3. Treatment of severe malaria

### Treatment of severe malaria

Treatment of severe malaria

It is essential that full doses of effective parenteral (or rectal) antimalarial treatment be given promptly in the initial treatment of

severe malaria. This should be followed by a full dose of effective ACT orally. Two classes of medicine are available for parenteral

treatment of severe malaria: artemisinin derivatives (artesunate or artemether) and the cinchona alkaloids (quinine and quinidine).

Parenteral artesunate is the trea...

📄 **Reference:** Page 211

### 4. Systematic review summary

### Systematic review summary

Systematic review summary

Six studies form the basis of these recommendations: five were individual randomized controlled trials (RCTs) and one was an open-

label extension study of an included RCT. One RCT was a multicentre study evaluating three or four doses of the RTS,S/AS01 malaria

vaccine compared to no malaria vaccination. One RCT evaluated the seasonal administration of RTS,S/AS01 malaria vaccine alone

compared to SMC alone, and also compared a combinat...

📄 **Reference:** Page 386

### 5. Benefits and harms

### Benefits and harms

Benefits and harms

Malaria vaccines, provided in a four-dose schedule, have been demonstrated in clinical trials to significantly

reduce clinical malaria, providing substantial added protection to that already given by existing malaria

preventive measures (i.e. ITNs and/or seasonal malaria chemoprevention (SMC)). In addition, pilot

implementation showed that the introduction of the vaccine through routine childhood immunization

programmes in Ghana, Kenya and Malawi r...

📄 **Reference:** Page 157


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 157, Page 211, Page 268, Page 386, Page 458

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 13. Query

> Fluid management in severe malaria adults

**Sources (top hits)**
- Page 213: Additional aspects of management
- Page 212: Management of complications
- Page 211: Clinical assessment
- Page 218: Benefits and harms
- Page 404: Publication bias: no serious.

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Fluid management in severe malaria adults

### 1. Additional aspects of management

### Additional aspects of management

Additional aspects of management

Fluid therapy

Fluid requirements should be assessed individually. Adults with severe malaria are very vulnerable to fluid overload, while children

are more likely to be dehydrated. The fluid regimen must also be adapted to the infusion of antimalarial drugs. Rapid bolus infusion

of colloid or crystalloids is contraindicated. If available, haemofiltration should be started early for acute kidney injury or severe

metabolic...

📄 **Reference:** Page 213

### 2. Management of complications

### Management of complications

Management of complications

Severe malaria is associated with a variety of manifestations and complications, which must be recognized promptly and treated

as shown below.

Immediate clinical management of severe manifestations and complications of P. falciparum malaria...

📄 **Reference:** Page 212

### 3. Clinical assessment

### Clinical assessment

Clinical assessment

Severe malaria is a medical emergency. An open airway should be secured in unconscious patients and breathing and circulation

assessed. The patient should be weighed or body weight estimated, so that medicines, including antimalarial drugs and fluids, can

be given appropriately. An intravenous cannula should be inserted, and blood glucose (rapid test), haematocrit or haemoglobin,

parasitaemia and, in adults, renal function should be measured immed...

📄 **Reference:** Page 211

### 4. Benefits and harms

### Benefits and harms

Benefits and harms

Is parenteral artesunate superior to parenteral quinine in preventing death from severe malaria?

Desirable effects:

•

In children > 12 years and adults, parenteral artesunate probably prevents more deaths than

intramuscular artemether (moderate-quality evidence).

•

No randomized controlled trials have been conducted in children aged ≤ 12 years.

--

Is intramuscular artemether superior to parenteral quinine in preventing death from severe malaria...

📄 **Reference:** Page 218

### 5. Publication bias: no serious.

### Publication bias: no serious.

defined as radiographically proven pneumonia, meningitis established by analysis of cerebrospinal fluid, sepsis (with positive blood

culture), or gastroenteritis with severe dehydration). Laboratory tests and other examinations (chest x-ray, lumbar puncture, blood

culture) to exclude co-morbidities were performed only if there was a clinical suspicion/diagnosis justifying additional investigations.

The study included 450 total participants with three study a...

📄 **Reference:** Page 404


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 211, Page 212, Page 213, Page 218, Page 404

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 14. Query

> Exchange transfusion malaria criteria

**Sources (top hits)**
- Page 213: Additional aspects of management
- Page 128: Untitled
- Page 235: Research needs
- Page 245: Research needs
- Page 150: Research needs

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Exchange transfusion malaria criteria

### 1. Additional aspects of management

### Additional aspects of management

Additional aspects of management

Fluid therapy

Fluid requirements should be assessed individually. Adults with severe malaria are very vulnerable to fluid overload, while children

are more likely to be dehydrated. The fluid regimen must also be adapted to the infusion of antimalarial drugs. Rapid bolus infusion

of colloid or crystalloids is contraindicated. If available, haemofiltration should be started early for acute kidney injury or severe

metabolic...

📄 **Reference:** Page 213

### 2. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

post-discharge. The main outcomes of interest were the impact of PDMC on re-admission (all-cause and severe anaemia),

mortality (all-cause), severe anaemia, and blood transfusion. Other outcomes of interest included confirmed clinical malaria,

severe malaria, anaemia, adverse events, and parasite prevalence. Three randomized double-blind placebo-controlled trials were

included in the review. All the trials were con...

📄 **Reference:** Page 128

### 3. Research needs

### Research needs

Research needs

•

Further evidence is needed on the impact (prevalence and incidence of malaria infection at the community level ) and

potential harms/unintended consequences of TDA for malaria in very low to low transmission or post-elimination settings.

•

Evidence is needed on the acceptability, feasibility, impact (prevalence and incidence of malaria infection at the community

level) and potential harms/unintended consequences (death, hospital admission, severe anaemi...

📄 **Reference:** Page 235

### 4. Research needs

### Research needs

Research needs

•

Further evidence is needed on the impact (prevalence and incidence of malaria infection at the community level) and potential

harms/unintended consequences of RDA.

•

Evidence is needed on the acceptability, feasibility, impact (prevalence and incidence of malaria infection at the community

level) and potential harms/unintended consequences (death, hospital admission, severe anaemia or any severe adverse

event) of safe provision (including testing for G...

📄 **Reference:** Page 245

### 5. Research needs

### Research needs

Research needs

•

Further evidence is needed on the impact (incidence or prevalence of malaria infection at the community level) and

potential harms/ unintended consequences of MDA for P. vivax.

•

Evidence is needed on the acceptability, feasibility, impact (incidence or prevalence of malaria infection at the community

level) and potential harms/unintended consequences (death, hospital admission, severe anaemia or any severe adverse

event) of safe provision (including t...

📄 **Reference:** Page 150


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 128, Page 150, Page 213, Page 235, Page 245

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 15. Query

> Cerebral malaria supportive care

**Sources (top hits)**
- Page 210: 5.2.2 Treating severe malaria
- Page 212: Continuing supportive care
- Page 220: Continuing supportive care
- Page 211: Therapeutic objectives
- Page 411: Publication bias: no serious.

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Cerebral malaria supportive care

### 1. 5.2.2 Treating severe malaria

### 5.2.2 Treating severe malaria

5.2.2 Treating severe malaria

Mortality from untreated severe malaria (particularly cerebral malaria) approaches 100%. With prompt, effective antimalarial

treatment and supportive care, the rate falls to 10–20% overall. Within the broad definition of severe malaria some syndromes are

associated with lower mortality rates (e.g. severe anaemia) and others with higher mortality rates (e.g. acidosis). The risk for death

increases in the presence of multiple com...

📄 **Reference:** Page 210

### 2. Continuing supportive care

### Continuing supportive care

Continuing supportive care

Patients with severe malaria require intensive nursing care, preferably in an intensive care unit where possible. Clinical

observations should be made as frequently

as possible and should include monitoring of vital signs, coma score and urine output.

Blood glucose should be monitored every 4 h, if possible, particularly in unconscious patients....

📄 **Reference:** Page 212

### 3. Continuing supportive care

### Continuing supportive care

Continuing supportive care

Patients with severe malaria require intensive nursing care, preferably in an intensive care unit where possible. Clinical

observations should be made as frequently

as possible and should include monitoring of vital signs, coma score and urine

output. Blood glucose should be monitored every 4 h, if possible, particularly in unconscious patients.

Please refer to The use of rectal artesunate as a pre-referral treatment for severe Plas...

📄 **Reference:** Page 220

### 4. Therapeutic objectives

### Therapeutic objectives

Therapeutic objectives

The main objective of the treatment of severe malaria is to prevent the patient from dying. Secondary objectives are prevention of

disabilities and prevention of recrudescent infection.

Death from severe malaria often occurs within hours of admission to a hospital or clinic, so it is essential that therapeutic

concentrations of a highly effective antimalarial drug be achieved as soon as possible. Management of severe malaria comprises

mainl...

📄 **Reference:** Page 211

### 5. Publication bias: no serious.

### Publication bias: no serious.

142. Inconsistency: no serious. Indirectness: no serious. Imprecision: serious. Downgraded two levels for imprecision: zero

events in the control group. Publication bias: no serious.

143. [Safety outcome] Cerebral malaria assessed with positive P. falciparum rapid diagnostic test or by microscopy, with impaired

consciousness (Glasgow coma score <11 or Blantyre coma score <3 or assessed as P or U on the AVPU scale (“Alert, Voice, Pain,

Unresponsive”). Pilot ...

📄 **Reference:** Page 411


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 210, Page 211, Page 212, Page 220, Page 411

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 16. Query

> Artesunate dose for severe malaria IV

**Sources (top hits)**
- Page 155: Schedule
- Page 211: Treatment of severe malaria
- Page 22: Untitled
- Page 217: Artemether
- Page 220: Pre-referral treatment options (2015)

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Artesunate dose for severe malaria IV

### 1. Schedule

### Schedule

Schedule

Malaria vaccines should be provided in a four-dose schedule in children from 5 months of age for the reduction of malaria disease and

burden. Countries may choose to give the first vaccine dose earlier than 5 months of age on the basis of operational considerations, to

increase coverage or impact.[iv]

The minimum interval between any doses is four weeks; however, to achieve prolonged protection, the fourth dose should be given

6–18 months after the third dose. To impr...

📄 **Reference:** Page 155

### 2. Treatment of severe malaria

### Treatment of severe malaria

Treatment of severe malaria

It is essential that full doses of effective parenteral (or rectal) antimalarial treatment be given promptly in the initial treatment of

severe malaria. This should be followed by a full dose of effective ACT orally. Two classes of medicine are available for parenteral

treatment of severe malaria: artemisinin derivatives (artesunate or artemether) and the cinchona alkaloids (quinine and quinidine).

Parenteral artesunate is the trea...

📄 **Reference:** Page 211

### 3. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

Where complete treatment of severe malaria is not possible, but injections are available, adults and children

should be given a single intramuscular dose of artesunate, and referred to an appropriate facility for further care.

Where intramuscular artesunate is not available, intramuscular artemether or, if that is not available,

intramuscular quinine should be used.

Where intramuscular injection of artesunate is n...

📄 **Reference:** Page 22

### 4. Artemether

### Artemether

Artemether

Artemether is two to three times less active than its main metabolite dihydroartemisinin. Artemether can be given as an oil-

based intramuscular injection or orally. In severe falciparum malaria, the concentration of the parent compound predominates

after intramuscular injection, whereas parenteral artesunate is hydrolysed rapidly and almost completely to dihydroartemisinin.

Given intramuscularly, artemether may be absorbed more slowly and more erratically than wat...

📄 **Reference:** Page 217

### 5. Pre-referral treatment options (2015)

### Pre-referral treatment options (2015)

Pre-referral treatment options (2015)

Where complete treatment of severe malaria is not possible, but injections are available, adults and children should be given a

single intramuscular dose of artesunate, and referred to an appropriate facility for further care. Where intramuscular artesunate

is not available, intramuscular artemether or, if that is not available, intramuscular quinine should be used.

Where intramuscular injection of artesunate is...

📄 **Reference:** Page 220


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 22, Page 155, Page 211, Page 217, Page 220

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 17. Query

> Rectal artesunate pre-referral children

**Sources (top hits)**
- Page 219: 5.2.2.3 Pre-referral treatment options
- Page 221: GRADE
- Page 187: Untitled
- Page 220: Pre-referral treatment options (2015)
- Page 221: Other considerations

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Rectal artesunate pre-referral children

### 1. 5.2.2.3 Pre-referral treatment options

### 5.2.2.3 Pre-referral treatment options

5.2.2.3 Pre-referral treatment options

The risk for death from severe malaria is greatest in the first 24 h, yet, in most malaria-endemic countries, the transit time

between referral and arrival at a health facility where intravenous treatment can be administered is usually long, thus delaying

the start of appropriate antimalarial treatment. During this time, the patient may deteriorate or die. It is therefore recommended

that patients, particularl...

📄 **Reference:** Page 219

### 2. GRADE

### GRADE

GRADE

In a systematic review of pre-referral treatment for suspected severe malaria, in a single large randomized controlled trial of 17

826 children and adults in Bangladesh, Ghana and the United Republic of Tanzania, pre-referral rectal artesunate was

compared with placebo [286].

In comparison with placebo:

•

Rectal artesunate reduced mortality by about 25% in children < 6 years (RR, 0.74; 95% CI, 0.59–0.93; one trial, 8050

participants, moderate- quality evidence).

•

Recta...

📄 **Reference:** Page 221

### 3. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

exposure in this vulnerable population. The available evidence for artemether + lumefantrine, SP and chloroquine does not

indicate dose modification at this time, but young children should be closely monitored, as reduced drug exposure may

increase the risk for treatment failure. Limited studies of amodiaquine and mefloquine showed no significant effect of age

on plasma concentration profiles.

In community situati...

📄 **Reference:** Page 187

### 4. Pre-referral treatment options (2015)

### Pre-referral treatment options (2015)

Pre-referral treatment options (2015)

Where complete treatment of severe malaria is not possible, but injections are available, adults and children should be given a

single intramuscular dose of artesunate, and referred to an appropriate facility for further care. Where intramuscular artesunate

is not available, intramuscular artemether or, if that is not available, intramuscular quinine should be used.

Where intramuscular injection of artesunate is...

📄 **Reference:** Page 220

### 5. Other considerations

### Other considerations

Other considerations

The guideline development group could find no plausible explanation for the finding of increased mortality among older

children and adults in Asia who received rectal artesunate, which may be due to chance. Further trials would provide

clarification but are unlikely to be done. The group was therefore unable to recommend its use in older children and adults.

In the absence of direct evaluations of parenteral antimalarial drugs for pre- referral ...

📄 **Reference:** Page 221


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 187, Page 219, Page 220, Page 221

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 18. Query

> Malaria in HIV coinfection

**Sources (top hits)**
- Page 188: 5.2.1.4.3 Patients co-infected with HIV
- Page 156: Vaccination of special populations
- Page 230: Acceptability
- Page 443: 5.2.1.4.3. Patients co-infected with HIV
- Page 164: Diagnosis of malaria

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Malaria in HIV coinfection

### 1. 5.2.1.4.3 Patients co-infected with HIV

### 5.2.1.4.3 Patients co-infected with HIV

5.2.1.4.3 Patients co-infected with HIV

There is considerable geographical overlap between malaria and HIV infection, and many people are co-infected.

Worsening HIV-related immunosuppression may lead to more severe manifestations of malaria. In HIV-infected pregnant

women, the adverse effects of placental malaria on birth weight are increased. In areas of stable endemic malaria, HIV-

infected patients who are partially immune to malaria may have m...

📄 **Reference:** Page 188

### 2. Vaccination of special populations

### Vaccination of special populations

Vaccination of special populations

Malnourished children may be at particular risk of malaria infection and can be vaccinated with either vaccine. RTS,S/AS01 can be

given to children with HIV infection.

RTS,S/AS01 has been evaluated in infants with a history of preterm birth (before 37 weeks’ gestation) and/or low birth weight, in HIV-

exposed or in HIV-infected infants and children, and in malnourished infants and children. The vaccine was found to be...

📄 **Reference:** Page 156

### 3. Acceptability

### Acceptability

Acceptability

The acceptability of MTaT was reported in three qualitative studies identified by the systematic review

(Bhamani et al unpublished evidence). One study in western Kenya found that the community engaged in

an MTaT intervention reported concerns over testing in the absence of symptoms. These concerns were

mostly related to the fear of covert HIV testing and some lack of understanding of the possibility of

asymptomatic malaria. Other issues related to acceptabi...

📄 **Reference:** Page 230

### 4. 5.2.1.4.3. Patients co-infected with HIV

### 5.2.1.4.3. Patients co-infected with HIV

5.2.1.4.3. Patients co-infected with HIV...

📄 **Reference:** Page 443

### 5. Diagnosis of malaria

### Diagnosis of malaria

Diagnosis of malaria

In patients with suspected severe malaria and in other high-risk groups, such as patients living with HIV/AIDS, absence or delay of

parasitological diagnosis should not delay an immediate start of antimalarial treatment.

At present, molecular diagnostic tools based on nucleic-acid amplification techniques (e.g. loop-mediated isothermal amplification or

polymerase chain reaction [PCR]) do not have a role in the clinical management of malaria.

Wh...

📄 **Reference:** Page 164


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 156, Page 164, Page 188, Page 230, Page 443

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 19. Query

> Species Plasmodium vivax relapse treatment

**Sources (top hits)**
- Page 190: knowlesi
- Page 310: Untitled
- Page 34: Etiology
- Page 311: Untitled
- Page 153: Malaria vaccine pipeline

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Species Plasmodium vivax relapse treatment

### 1. knowlesi

### knowlesi

5.2.1.5 Uncomplicated malaria caused by P. vivax, P. ovale, P. malariae or P.

knowlesi

Plasmodium vivax accounts for approximately half of all malaria cases outside Africa [3][250][251]. It is prevalent in the Middle

East, Asia, the Western Pacific and Central and South America. With the exception of the Horn, it is rarer in Africa, where there

is a high prevalence of the Duffy-negative phenotype, particularly in West Africa, although cases are reported in both

Mauritania and ...

📄 **Reference:** Page 190

### 2. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

in early infancy. Clinical infectious diseases : an official publication of the Infectious Diseases Society of America 2009;48(12):1704-12

Pubmed Journal

256. Genton B, D'Acremont V, Rare L, Baea K, Reeder JC, Alpers MP, et al. Plasmodium vivax and mixed infections are associated with

severe malaria in children: a prospective cohort study from Papua New Guinea. PLoS medicine 2008;5(6):e127 Pubmed Journal

257. Koch...

📄 **Reference:** Page 310

### 3. Etiology

### Etiology

Etiology

Malaria is a life-threatening disease caused by the infection of red blood cells with protozoan parasites of the genus Plasmodium that are

transmitted to people through the bites of infected female Anopheles mosquitoes. Four species of Plasmodium (P. falciparum, P. vivax, P.

malariae and P. ovale) most commonly infect humans. P. falciparum and P. vivax are the most prevalent species and P. falciparum is the

most dangerous. A fifth species, P. knowlesi (a species of Pla...

📄 **Reference:** Page 34

### 4. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

272. Verma R, Commons RJ, Gupta A, Rahi M, Nitika, Bharti PK, et al. Safety and efficacy of primaquine in patients with Plasmodium

vivax malaria from South Asia: a systematic review and individual patient data meta-analysis. BMJ global health 2023;8(12) Pubmed

Journal

273. Mehdipour P, Rajasekhar M, Dini S, Zaloumis S, Abreha T, Adam I, et al. Effect of adherence to primaquine on the risk of

Plasmodium vivax recur...

📄 **Reference:** Page 311

### 5. Malaria vaccine pipeline

### Malaria vaccine pipeline

Malaria vaccine pipeline

Two malaria vaccines are WHO-prequalified and recommended for use: RTS,S/AS01 and R21/Matrix-M. Both are pre-erythrocytic

vaccines that prevent P. falciparum infection and subsequent illness and death in children; the vaccines are not designed to interrupt

malaria transmission. The recommended malaria vaccines prevent P. falciparum malaria. There is no known cross-protection with

other Plasmodium species. However, in areas where P. falci...

📄 **Reference:** Page 153


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 34, Page 153, Page 190, Page 310, Page 311

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 20. Query

> Monitoring after antimalarial treatment failure

**Sources (top hits)**
- Page 224: Therapeutic efficacy
- Page 22: Monitoring efficacy and safety of antimalarial drugs and resistance (2010)
- Page 224: Monitoring efficacy and safety of antimalarial drugs and resistance (2010)
- Page 22: National adaptation and implementation (2010)
- Page 227: National adaptation and implementation (2010)

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Monitoring after antimalarial treatment failure

### 1. Therapeutic efficacy

### Therapeutic efficacy

Therapeutic efficacy

Monitoring of therapeutic efficacy in falciparum malaria involves assessing clinical and parasitological outcomes of treatment

for at least 28 days after the start of adequate treatment and monitoring for the reappearance of parasites in blood. The exact

duration of post-treatment follow-up is based on the elimination half- life of the partner drug in the ACT being evaluated. Tools

for monitoring antimalaria drug efficacy can be found on the WHO...

📄 **Reference:** Page 224

### 2. Monitoring efficacy and safety of antimalarial drugs and resistance (2010)

### Monitoring efficacy and safety of antimalarial drugs and resistance (2010)

Monitoring efficacy and safety of antimalarial drugs and resistance (2010)

All malaria programmes should regularly monitor the therapeutic efficacy of antimalarial drugs using the standard

WHO protocols.

An antimalarial medicine that is recommended in the national malaria treatment policy should be changed if the

total treatment failure proportion is ≥ 10%, as assessed in vivo by monitoring therapeutic efficacy.
...

📄 **Reference:** Page 22

### 3. Monitoring efficacy and safety of antimalarial drugs and resistance (2010)

### Monitoring efficacy and safety of antimalarial drugs and resistance (2010)

Monitoring efficacy and safety of antimalarial drugs and resistance (2010)

All malaria programmes should regularly monitor the therapeutic efficacy of antimalarial drugs using the standard WHO

protocols.

An antimalarial medicine that is recommended in the national malaria treatment policy should be changed if the total treatment

failure proportion is ≥ 10%, as assessed in vivo by monitoring therapeutic efficacy.
...

📄 **Reference:** Page 224

### 4. National adaptation and implementation (2010)

### National adaptation and implementation (2010)

National adaptation and implementation (2010)

The choice of ACTs in a country or region should be based on optimal efficacy, safety and adherence.

An antimalarial medicine that is recommended in the national malaria treatment policy should be changed if the total

treatment failure proportion is ≥ 10%, as assessed in vivo by monitoring therapeutic efficacy.

Introduction of a new antimalarial medicine in the national treatment policy should be...

📄 **Reference:** Page 22

### 5. National adaptation and implementation (2010)

### National adaptation and implementation (2010)

National adaptation and implementation (2010)

The choice of ACTs in a country or region should be based on optimal efficacy, safety and adherence.

An antimalarial medicine that is recommended in the national malaria treatment policy should be changed if the total treatment failure

proportion is ≥ 10%, as assessed in vivo by monitoring therapeutic efficacy.

Introduction of a new antimalarial medicine in the national treatment policy should be...

📄 **Reference:** Page 227


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 22, Page 224, Page 227

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 21. Query

> Quality assurance microscopy

**Sources (top hits)**
- Page 165: Untitled
- Page 225: General guiding principles for choosing a case management strategy and tools
- Page 164: Parasitological diagnosis
- Page 196: Guidance
- Page 307: Untitled

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Quality assurance microscopy

### 1. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

•

high sensitivity, if the performance of microscopy is high;

•

differentiation of Plasmodia species;

•

determination of parasite densities – notably identification of hyperparasitaemia;

•

detection of gametocytaemia;

•

allows monitoring of responses to therapy and

•

can be used to diagnose many other conditions.

Good performance of microscopy can be difficult to maintain, because of the requirements for a...

📄 **Reference:** Page 165

### 2. General guiding principles for choosing a case management strategy and tools

### General guiding principles for choosing a case management strategy and tools

General guiding principles for choosing a case management strategy and tools

Choosing a diagnostic strategy

The two methods currently considered suitable for routine patient management are light microscopy and RDTs. Different strategies

may be adopted in different health care settings. The choice between RDTs and microscopy depends on local circumstances,

including the skills available, the patient case-load, t...

📄 **Reference:** Page 225

### 3. Parasitological diagnosis

### Parasitological diagnosis

Parasitological diagnosis

The benefit of parasitological diagnosis relies entirely on an appropriate management response of health care providers. The two

methods used routinely for parasitological diagnosis of malaria are light microscopy and immunochromatographic RDTs. The latter

detect parasite-specific antigens or enzymes that are either genus or species specific.

Both microscopy and RDTs must be supported by a quality assurance programme. Antimalarial trea...

📄 **Reference:** Page 164

### 4. Guidance

### Guidance

Guidance

The practical guidance on the use of qualitative near-patient tests for G6PD deficiency should include

all aspects of safe implementation of a new diagnostic test e.g. implementation plan, clear national

guidelines, quality assurance and prequalification of tests, training of users, quality assurance of

testing, and selection of the type of health services where these tests should be deployed. In addition

the guidance should also include specific information on the an...

📄 **Reference:** Page 196

### 5. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

200. Malaria diagnosis: memorandum from a WHO meeting. Bulletin of the World Health Organization 1988;66(5):575-94 Pubmed

201. Malaria microscopy quality assurance manual, version 2. Geneva: World Health Organization 2016. Website

202. Kawamoto F, Billingsley PF. Rapid diagnosis of malaria by fluorescence microscopy. Parasitology today (Personal ed.)

1992;8(2):69-71 Pubmed

203. Malaria diagnosis: new perspectives....

📄 **Reference:** Page 307


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 164, Page 165, Page 196, Page 225, Page 307

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 22. Query

> Integrated community case management fever

**Sources (top hits)**
- Page 164: Untitled
- Page 227: Other operational issues in managing effective treatment
- Page 225: General guiding principles for choosing a case management strategy and tools
- Page 37: Global vector control response 2017–2030
- Page 28: Untitled

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Integrated community case management fever

### 1. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

In malaria-endemic areas, malaria should be suspected in any patient presenting with a history of fever or temperature ≥ 37.5 °C and

no other obvious cause. In areas in which malaria transmission is stable (or during the high-transmission period of seasonal malaria),

malaria should also be suspected in children with palmar pallor or a haemoglobin concentration of < 8 g/dL. High-transmission settings

include many pa...

📄 **Reference:** Page 164

### 2. Other operational issues in managing effective treatment

### Other operational issues in managing effective treatment

Other operational issues in managing effective treatment

Individual patients derive the maximum benefit from an ACT if they can access it within 24–48 h of the onset of malaria symptoms.

The impact in reducing transmission at a population level depends on high coverage rates and the transmission intensity. Thus, to

optimize the benefits of deploying ACTs, they should be available in the public health delivery system, the private se...

📄 **Reference:** Page 227

### 3. General guiding principles for choosing a case management strategy and tools

### General guiding principles for choosing a case management strategy and tools

General guiding principles for choosing a case management strategy and tools

Choosing a diagnostic strategy

The two methods currently considered suitable for routine patient management are light microscopy and RDTs. Different strategies

may be adopted in different health care settings. The choice between RDTs and microscopy depends on local circumstances,

including the skills available, the patient case-load, t...

📄 **Reference:** Page 225

### 4. Global vector control response 2017–2030

### Global vector control response 2017–2030

Global vector control response 2017–2030

The vision of WHO and the broader infectious diseases community is a world free of human suffering from vector-borne diseases. In

2017, the World Health Assembly welcomed the Global vector control response 2017–2030 [16] (GVCR) and adopted a resolution to

promote an integrated approach to the control of vector-borne diseases. The approach builds on the concept of integrated vector

management (IVM), but wit...

📄 **Reference:** Page 37

### 5. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

G6PD

glucose-6-phosphate dehydrogenase

HBHI

High burden to high impact approach

HFCA

health-facility catchment area

HRP2

histidine-rich protein 2

ICER

incremental cost-effectiveness ratio

IHR

International Health Regulation

IPTi

intermittent preventive treatment in infants, now referred to as perennial malaria chemoprevention (PMC)

IPTp

intermittent preventive treatment in pregnancy

IPTsc

intermittent...

📄 **Reference:** Page 28


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 28, Page 37, Page 164, Page 225, Page 227

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 23. Query

> Ethics of placebo-controlled malaria trials

**Sources (top hits)**
- Page 280: Untitled
- Page 108: Untitled
- Page 453: parasitaemia
- Page 453: Anaemia in third
- Page 128: Untitled

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Ethics of placebo-controlled malaria trials

### 1. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

•

Dr Anna Maria van Eijk, Liverpool School of Tropical Medicine, Liverpool, United Kingdom of Great Britain and Northern Ireland

Perennial Malaria Chemoprevention (PMC) (formerly Intermittent Preventive Treatment in infants or IPTi)

•

Dr Christina Carlson, Division of Parasitic Diseases and Malaria, Centers for Disease Control and Prevention, Atlanta, United

States of America

•

Dr Laura Steinhardt, Malaria Bran...

📄 **Reference:** Page 280

### 2. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

supplemented by a cross-cutting review on chemoprevention and drug resistance (Plowe unpublished evidence), a civil society

consultation report on chemoprevention (CS4ME unpublished evidence) and contributions from the GDG membership, which

included former and current national malaria programme representatives. The GDG was supported by a Steering Group, which

included representatives from the WHO Departments for Se...

📄 **Reference:** Page 108

### 3. parasitaemia

### parasitaemia

P. vivax

parasitaemia

Relative risk 0.02

(CI 95% 0 — 0.26)

Based on data from 951

participants in 1 studies.

(Randomized controlled)...

📄 **Reference:** Page 453

### 4. Anaemia in third

### Anaemia in third

Anaemia in third

Relative risk 0.95

(CI 95% 0.9 — 1.01)

Based on data from 951

participants in 1 studies.

(Randomized controlled)...

📄 **Reference:** Page 453

### 5. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

post-discharge. The main outcomes of interest were the impact of PDMC on re-admission (all-cause and severe anaemia),

mortality (all-cause), severe anaemia, and blood transfusion. Other outcomes of interest included confirmed clinical malaria,

severe malaria, anaemia, adverse events, and parasite prevalence. Three randomized double-blind placebo-controlled trials were

included in the review. All the trials were con...

📄 **Reference:** Page 128


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 108, Page 128, Page 280, Page 453

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 24. Query

> Vector control bed nets IRS

**Sources (top hits)**
- Page 297: Untitled
- Page 298: Untitled
- Page 338: measurements
- Page 68: Acceptability
- Page 41: 4.1.1 Interventions recommended for large-scale deployment

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Vector control bed nets IRS

### 1. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

26. REX Consortium. Heterogeneity of selection and the evolution of resistance. Trends in ecology & evolution 2013;28(2):110-8 Pubmed

Journal

27. Sternberg ED, Thomas MB. Insights from agriculture for the management of insecticide resistance in disease vectors. Evolutionary

applications 2018;11(4):404-414 Pubmed Journal

28. Huijben S, Paaijmans KP. Putting evolution in elimination: Winning our ongoing battle with ...

📄 **Reference:** Page 297

### 2. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

44. Snow RW, Lindsay SW, Hayes RJ, Greenwood BM. Permethrin-treated bed nets (mosquito nets) prevent malaria in Gambian children.

Transactions of The Royal Society of Tropical Medicine and Hygiene 1988;82(6):838-842 Pubmed Journal Website

45. Russell TL, Lwetoijera DW, Maliti D, Chipwaza B, Kihonda J, Charlwood JD, et al. Impact of promoting longer-lasting insecticide

treatment of bed nets upon malaria transmission...

📄 **Reference:** Page 298

### 3. measurements

### measurements

measurements

IRS

IRS

0.01) in intervention villages. (Data on

numbers of participants at follow-up not

provided)...

📄 **Reference:** Page 338

### 4. Acceptability

### Acceptability

Acceptability

The systematic review reported that wall decolourization, bad smell, an increase in bed bug nuisance,

and contamination of food grains were reported by study participants in India after spraying with

DDT [78]. However, these factors may depend on the insecticide and formulation used. In another study

conducted in Pakistan [56], no persistent odour or residue was reported after spraying with the pyrethroid

insecticide alpha-cypermethrin. In this same study, i...

📄 **Reference:** Page 68

### 5. 4.1.1 Interventions recommended for large-scale deployment

### 4.1.1 Interventions recommended for large-scale deployment

4.1.1 Interventions recommended for large-scale deployment

Interventions that are recommended for large-scale deployment in terms of malaria vector control are those that have proven

protective efficacy to reduce or prevent infection and/or disease in humans and are broadly applicable for populations at risk of

malaria in most epidemiological and ecological settings.

Vector control interventions applicable for all populations at...

📄 **Reference:** Page 41


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 41, Page 68, Page 297, Page 298, Page 338

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---

### 25. Query

> Elimination strategies and surveillance

**Sources (top hits)**
- Page 228: 6. Interventions in the final phase of elimination and prevention of re-establishment
- Page 30: Scope
- Page 146: (2022)
- Page 15: (2022)
- Page 36: Untitled

**Response**

```
**WHO Malaria Guidelines (NCBI Bookshelf)**

**Question:** Elimination strategies and surveillance

### 1. 6. Interventions in the final phase of elimination and prevention of re-establishment

### 6. Interventions in the final phase of elimination and prevention of re-establishment

6. Interventions in the final phase of elimination and prevention of re-establishment

The Global technical strategy for malaria 2016-2030 [4] urges all malaria-endemic countries to accelerate towards elimination and

attainment of malaria-free status. WHO recommends that all countries ensure access to malaria prevention, diagnosis and treatment as

part of universal health coverage; recommendations relate...

📄 **Reference:** Page 228

### 2. Scope

### Scope

Scope

The consolidated WHO Guidelines for malaria bring together all recommendations for malaria, including prevention using vector control,

preventive chemotherapy and the vaccine; diagnosis, treatment and elimination strategies. The Guidelines also provide links to other

resources including unpublished evidence reviewed at the time of formulating recommendations, guidance and information on strategic

use of information to drive impact, surveillance, monitoring and evaluation, op...

📄 **Reference:** Page 30

### 3. (2022)

### (2022)

MDA to reduce transmission of P. vivax (2022)

In areas with P. vivax transmission, antimalarial medicine can be given as chemoprevention through mass drug administration

(MDA) to reduce transmission.

•

MDA may quickly reduce transmission of P. vivax, but the effect wanes within 1–3 months. Therefore, if MDA is

implemented, it should be one of several components of a robust malaria elimination programme (including, at minimum,

good coverage of case-based surveillance with parasi...

📄 **Reference:** Page 146

### 4. (2022)

### (2022)

MDA to reduce transmission of P. vivax (2022)

In areas with P. vivax transmission, antimalarial medicine can be given as chemoprevention through mass drug

administration (MDA) to reduce transmission.

Remark:

•

MDA may quickly reduce transmission of P. vivax, but the effect wanes within 1–3 months. Therefore, if MDA is

implemented, it should be one of several components of a robust malaria elimination programme (including, at

minimum, good coverage of case-based surveillance wi...

📄 **Reference:** Page 15

### 5. Untitled

WHO guidelines for malaria - 13 August 2025 - World Health Organization (WHO)

problem-solving approach using local data to identify recommendations that are relevant at a country level and based on local

context, defining stratum-specific packages of interventions that optimize impact and are prioritized for resource allocation. This shift

moves away from overly prescriptive recommendations and will clearly distinguish evidence-informed recommendations from contextual

considerations. The con...

📄 **Reference:** Page 36


---

Triage Level: GREEN (evidence retrieval summary — not a substitute for bedside assessment; follow local protocols)

Immediate Actions: Review the guideline excerpts above; align actions with national/WHO guidance and qualified supervision.

Next Steps / Monitoring: Consult the full source guideline or a clinician for patient-specific decisions.

When to Refer: Per excerpts and national guidance; seek urgent care if danger signs, severe disease, or instability is suspected.

Citations: Page 15, Page 30, Page 36, Page 146, Page 228

---
**🧪 Guardrail Brain Validation:** ✅ Passed

```

**Guardrail**: passed=`True` | errors=0 | warnings=0

---
