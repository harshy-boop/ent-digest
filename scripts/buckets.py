from scripts.models import QueryBucket


BUCKETS: list[QueryBucket] = [
    QueryBucket(
        key="otology",
        label="Otology / Neurotology",
        query=(
            "(otologic[MeSH] OR ear diseases[MeSH] OR hearing loss[MeSH] "
            "OR cochlear implant* OR vestibular OR vertigo OR meniere* "
            "OR otosclerosis OR cholesteatoma OR mastoid* "
            "OR acoustic neuroma OR vestibular schwannoma OR lateral skull base)"
        ),
    ),
    QueryBucket(
        key="rhinology",
        label="Rhinology / Anterior Skull Base",
        query=(
            "(rhinology OR sinusitis OR nasal polyp* OR FESS "
            "OR endoscopic sinus OR endoscopic pituitary "
            "OR anterior skull base OR allergic rhinitis)"
        ),
    ),
    QueryBucket(
        key="laryngology",
        label="Laryngology / Voice / Dysphagia",
        query=(
            "(laryngology OR vocal cord OR vocal fold OR voice disorder* "
            "OR hoarseness OR dysphonia OR dysphagia OR swallowing "
            "OR deglutition disorders[MeSH])"
        ),
    ),
    QueryBucket(
        key="airway",
        label="Airway",
        query=(
            "(subglottic stenosis OR tracheal stenosis OR laryngotracheal "
            "OR airway reconstruction OR pediatric airway "
            "OR congenital airway OR cricoid)"
        ),
    ),
    QueryBucket(
        key="sleep",
        label="Sleep Surgery / OSA",
        query=(
            "(obstructive sleep apnea[MeSH] OR sleep-disordered breathing) AND "
            "(surgery OR surgical OR hypoglossal OR upper airway stimulation "
            "OR maxillomandibular OR UPPP OR uvulopalatopharyngoplasty "
            "OR DISE OR drug-induced sleep endoscopy "
            "OR pharyngeal surgery OR sleep apnea surgery)"
        ),
    ),
    QueryBucket(
        key="oncology",
        label="Head & Neck Surgical Oncology",
        query=(
            "(head and neck neoplasms[MeSH] OR oral cavity cancer OR oropharyngeal cancer "
            "OR laryngeal cancer OR hypopharyngeal cancer OR thyroid cancer "
            "OR salivary gland neoplasms[MeSH] OR parotid neoplasms[MeSH] "
            "OR \"HPV+ OPSCC\") AND "
            "(head OR neck OR oral OR oropharyn* OR laryng* OR hypopharyn* "
            "OR thyroid OR salivary OR parotid OR mandible OR maxilla)"
        ),
    ),
    QueryBucket(
        key="facial_plastic",
        label="Facial Plastic & Reconstructive",
        query=(
            "(rhinoplasty OR facelift OR blepharoplasty OR facial reconstruction "
            "OR craniofacial OR cleft lip OR cleft palate OR maxillofacial "
            "OR orbital fracture OR (free flap AND face))"
        ),
    ),
    QueryBucket(
        key="pediatric",
        label="Pediatric ENT",
        query=(
            "(pediatric OR child* OR infant*) AND "
            "(otolaryngolog* OR tonsil* OR adenoid* OR otitis OR airway "
            "OR laryng* OR tracheo* OR cleft OR craniofacial OR hearing)"
        ),
    ),
    QueryBucket(
        key="crossover",
        label="Practice-Changing Crossover",
        query=(
            "(\"N Engl J Med\"[Journal] OR \"JAMA\"[Journal] OR \"Lancet\"[Journal] "
            "OR \"BMJ\"[Journal] OR \"Ann Intern Med\"[Journal] OR \"Nat Med\"[Journal] "
            "OR \"Ann Surg\"[Journal] OR \"JAMA Surg\"[Journal]) AND "
            "(otolaryngol* OR ENT OR airway OR laryng* OR sinus* OR rhinolog* "
            "OR \"head and neck\" OR craniofacial OR cochlear OR cleft "
            "OR tracheo* OR sleep apnea)"
        ),
    ),
    QueryBucket(
        key="policy",
        label="Health Policy Literature",
        query=(
            "(\"Health Aff (Millwood)\"[Journal] OR \"JAMA Health Forum\"[Journal] "
            "OR \"Health Policy\"[Journal] OR \"Milbank Q\"[Journal] "
            "OR \"Health Serv Res\"[Journal]) AND "
            "(Medicare OR Medicaid OR \"insurance coverage\" OR reimbursement "
            "OR \"value-based\" OR surgery OR otolaryngol* OR \"head and neck\" "
            "OR ENT OR sleep apnea OR cochlear OR cleft)"
        ),
    ),
]
