LESSONS = [
    {
        "concept_slug": "cryptography",
        "title": "Cryptography Fundamentals",
        "slug": "new-cryptography-fundamentals",
        "description": "A deep dive into symmetric vs asymmetric encryption, hashing, digital signatures, and the critical mistakes that break real-world crypto systems.",
        "hook": "Your bank, your messages, your passwords — they all depend on cryptography. But what happens when the crypto is broken?",
        "problem": "Most developers treat encryption as a black box, leading to catastrophic mistakes like hardcoded keys, weak algorithms, and ECB mode usage.",
        "explanation": "Symmetric encryption (AES) uses one shared key, while asymmetric (RSA) uses a public-private key pair. Hashing (SHA-256, bcrypt) creates fixed-size fingerprints. Diffie-Hellman allows two parties to agree on a shared secret over an insecure channel. Digital signatures combine hashing and asymmetric encryption to prove authenticity.",
        "real_world_example": "WEP cracking became trivial because of weak initialization vectors and RC4 bias. Attackers could recover the WEP key in minutes. The Equifax breach was worsened by the Apache Struts vulnerability, but weak TLS configurations compounded the damage.",
        "summary": "Cryptography is the foundation of digital security, but only when implemented correctly. A single mistake — a weak key, a hardcoded IV, or an outdated algorithm — can collapse the entire system.",
        "curiosity_hook": "Did you know that the HTTPS lock icon in your browser means almost nothing if the server uses weak cipher suites?",
        "dialogue": [
            {"speaker": "Peter", "text": "So encryption is just scrambling data so nobody can read it, right?"},
            {"speaker": "Stewie", "text": "That's like saying surgery is just cutting people open. Context matters enormously."},
            {"speaker": "Peter", "text": "What's the difference between AES and RSA then?"},
            {"speaker": "Stewie", "text": "AES is fast symmetric encryption with one shared key. RSA is slow asymmetric with a public and private key pair."},
            {"speaker": "Peter", "text": "So why not just use RSA for everything?"},
            {"speaker": "Stewie", "text": "Because RSA is about a thousand times slower. You use RSA to exchange an AES key, then AES for the actual data."},
            {"speaker": "Peter", "text": "What about hashing? Is that the same as encryption?"},
            {"speaker": "Stewie", "text": "No, hashing is one-way. You can't reverse it. It's a fingerprint, not a lock."},
            {"speaker": "Peter", "text": "What's the biggest mistake people make with crypto?"},
            {"speaker": "Stewie", "text": "Rolling their own. Never invent your own encryption algorithm. Use battle-tested libraries."},
            {"speaker": "Peter", "text": "So the math can be perfect but the implementation can still fail?"},
            {"speaker": "Stewie", "text": "Exactly. Hardcoded IVs, weak keys, ECB mode — these are implementation sins. The devil is in the details."}
        ],
        "learning_objectives": [
            "Understand the difference between symmetric and asymmetric encryption and when to use each",
            "Explain how hashing, digital signatures, and key exchange protocols work",
            "Identify common cryptographic implementation mistakes and how to avoid them",
            "Recognize famous real-world cryptographic failures and their root causes"
        ],
        "quiz_questions": [
            {
                "question": "Why is ECB mode considered insecure for encrypting large amounts of data?",
                "answers": [
                    {"id": "a", "text": "It's too slow for production use", "correct": False},
                    {"id": "b", "text": "Identical plaintext blocks produce identical ciphertext blocks, leaking patterns", "correct": True},
                    {"id": "c", "text": "It requires a separate key for each block", "correct": False},
                    {"id": "d", "text": "It doesn't support padding schemes", "correct": False}
                ]
            },
            {
                "question": "Why is bcrypt preferred over SHA-256 for password hashing?",
                "answers": [
                    {"id": "a", "text": "bcrypt produces shorter hash values", "correct": False},
                    {"id": "b", "text": "bcrypt is faster and more efficient", "correct": False},
                    {"id": "c", "text": "bcrypt is deliberately slow with a work factor, making brute-force attacks harder", "correct": True},
                    {"id": "d", "text": "bcrypt uses asymmetric encryption", "correct": False}
                ]
            },
            {
                "question": "What is the primary purpose of Diffie-Hellman key exchange?",
                "answers": [
                    {"id": "a", "text": "To encrypt all communication between two parties", "correct": False},
                    {"id": "b", "text": "To allow two parties to agree on a shared secret over an insecure channel", "correct": True},
                    {"id": "c", "text": "To generate digital signatures for email", "correct": False},
                    {"id": "d", "text": "To replace the need for passwords", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "social-engineering",
        "title": "Social Engineering: The Human Hack",
        "slug": "new-social-engineering",
        "description": "How attackers exploit human psychology through pretexting, phishing, tailgating, and sophisticated social engineering campaigns.",
        "hook": "The most expensive firewall in the world is useless if someone holds the door open for an attacker.",
        "problem": "Organizations invest millions in technical defenses while neglecting the fact that over 80% of breaches involve a human element — social engineering.",
        "explanation": "Social engineering exploits human trust and urgency rather than technical vulnerabilities. Pretexting creates false scenarios, baiting uses curiosity, tailgating exploits politeness, and spear-phishing targets specific individuals with personalized lures. MITRE ATT&CK catalogues these techniques systematically.",
        "real_world_example": "The 2020 Twitter hack started with a phone-based social engineering attack against employees, giving attackers access to internal tools that compromised high-profile accounts including Elon Obama and Elon Musk. The SolarWinds attack began with spear-phishing an IT company employee.",
        "summary": "Social engineering remains the most effective attack vector because humans are predictable, trusting, and often too busy to verify. Technical controls help, but awareness and culture are the real defenses.",
        "curiosity_hook": "Did you know that con artists have been using the same social engineering tactics for centuries — only the technology changes?",
        "dialogue": [
            {"speaker": "Peter", "text": "So social engineering is basically just tricking people?"},
            {"speaker": "Stewie", "text": "It's the art of manipulating humans into divulging information. It predates computers by millennia."},
            {"speaker": "Peter", "text": "Like phishing emails? I get those all the time."},
            {"speaker": "Stewie", "text": "Phishing is just one tactic. Pretexting creates scenarios. Tailgating exploits politeness. Baiting uses curiosity."},
            {"speaker": "Peter", "text": "What's spear-phishing then?"},
            {"speaker": "Stewie", "text": "Phishing targeted at a specific person using personal details. Way more effective than generic mass emails."},
            {"speaker": "Peter", "text": "Has this actually worked on real companies?"},
            {"speaker": "Stewie", "text": "The 2020 Twitter hack started with a phone call. Attackers hijacked accounts of Obama, Musk, and Apple."},
            {"speaker": "Peter", "text": "That's terrifying. How do you defend against that?"},
            {"speaker": "Stewie", "text": "Verification protocols. Never trust a call or email without confirming through a separate channel."},
            {"speaker": "Peter", "text": "So the fanciest attack starts with the simplest trick?"},
            {"speaker": "Stewie", "text": "Always. MITRE ATT&CK has an entire matrix for social engineering. Humans are the attack surface."}
        ],
        "learning_objectives": [
            "Identify different social engineering tactics including pretexting, baiting, tailgating, and spear-phishing",
            "Understand why humans are considered the weakest link in cybersecurity",
            "Recognize the MITRE ATT&CK social engineering techniques and how they map to real attacks",
            "Learn defense strategies including verification protocols and security culture"
        ],
        "quiz_questions": [
            {
                "question": "What distinguishes spear-phishing from regular phishing?",
                "answers": [
                    {"id": "a", "text": "Spear-phishing uses phone calls instead of emails", "correct": False},
                    {"id": "b", "text": "Spear-phishing targets specific individuals with personalized content", "correct": True},
                    {"id": "c", "text": "Spear-phishing only targets government agencies", "correct": False},
                    {"id": "d", "text": "Spear-phishing is automatically detected by email filters", "correct": False}
                ]
            },
            {
                "question": "How did the attackers initially gain access during the 2020 Twitter hack?",
                "answers": [
                    {"id": "a", "text": "SQL injection on the login page", "correct": False},
                    {"id": "b", "text": "Brute-forcing admin passwords", "correct": False},
                    {"id": "c", "text": "Phone-based social engineering against employees", "correct": True},
                    {"id": "d", "text": "Zero-day exploit in the mobile app", "correct": False}
                ]
            },
            {
                "question": "Which social engineering tactic exploits a person's natural tendency to be polite and hold doors open?",
                "answers": [
                    {"id": "a", "text": "Pretexting", "correct": False},
                    {"id": "b", "text": "Tailgating", "correct": True},
                    {"id": "c", "text": "Baiting", "correct": False},
                    {"id": "d", "text": "Whaling", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "forensics",
        "title": "Digital Forensics Fundamentals",
        "slug": "new-digital-forensics",
        "description": "How digital evidence is collected, preserved, and analyzed while maintaining the chain of custody needed for legal proceedings.",
        "hook": "When a crime happens in the digital world, someone has to investigate it without accidentally destroying the evidence.",
        "problem": "Improper evidence handling can render crucial digital proof inadmissible in court, allowing criminals to walk free on technicalities.",
        "explanation": "Digital forensics follows strict procedures: establish chain of custody, preserve volatile data first (RAM, network connections), use write-blockers for disk imaging, verify integrity with cryptographic hashes, and document every step. Tools like Volatility analyze memory dumps while disk forensics reconstructs timelines.",
        "real_world_example": "In major breach investigations, memory forensics with Volatility has recovered malware samples that never touched disk, encryption keys, and evidence of lateral movement that traditional disk forensics would miss entirely.",
        "summary": "Digital forensics is both a science and an art — the procedures matter as much as the technical skills. One mistake in evidence handling can invalidate an entire investigation.",
        "curiosity_hook": "Did you know that pulling a USB drive out of a running computer destroys evidence that exists only in RAM?",
        "dialogue": [
            {"speaker": "Peter", "text": "So digital forensics is just looking at a computer after a crime?"},
            {"speaker": "Stewie", "text": "It's far more systematic. It's a legal and technical process of collecting, preserving, and analyzing digital evidence."},
            {"speaker": "Peter", "text": "What do you mean by chain of custody?"},
            {"speaker": "Stewie", "text": "A documented trail showing who handled the evidence, when, and what they did. Break the chain, and it's worthless in court."},
            {"speaker": "Peter", "text": "Why does volatile data matter?"},
            {"speaker": "Stewie", "text": "RAM contains processes, network connections, encryption keys — things that vanish the moment you pull the plug."},
            {"speaker": "Peter", "text": "How do you even copy a hard drive for evidence?"},
            {"speaker": "Stewie", "text": "Write-blockers prevent modification. You create a bit-for-bit image and verify it with cryptographic hashes."},
            {"speaker": "Peter", "text": "What about Volatility? Is that like a cleaning product?"},
            {"speaker": "Stewie", "text": "Ha. Volatility is a memory forensics framework. It extracts artifacts from RAM dumps — processes, malware, sockets."},
            {"speaker": "Peter", "text": "Can criminals hide their tracks?"},
            {"speaker": "Stewie", "text": "Anti-forensics exists — wiping, timestamp manipulation. But each leaves its own trace if you know where to look."}
        ],
        "learning_objectives": [
            "Understand the chain of custody and why it's critical for legal proceedings",
            "Differentiate between volatile and non-volatile data and know the collection priority order",
            "Explain how forensic imaging, hash verification, and timeline analysis work",
            "Recognize anti-forensics techniques and how investigators counter them"
        ],
        "quiz_questions": [
            {
                "question": "Why is volatile data collected before non-volatile data in a forensic investigation?",
                "answers": [
                    {"id": "a", "text": "Volatile data is easier to access", "correct": False},
                    {"id": "b", "text": "Volatile data exists only in memory and is lost when the system powers down", "correct": True},
                    {"id": "c", "text": "Volatile data is always more important than disk data", "correct": False},
                    {"id": "d", "text": "Courts only accept volatile data as evidence", "correct": False}
                ]
            },
            {
                "question": "What is the purpose of a write-blocker during forensic disk imaging?",
                "answers": [
                    {"id": "a", "text": "To speed up the copying process", "correct": False},
                    {"id": "b", "text": "To encrypt the evidence while copying", "correct": False},
                    {"id": "c", "text": "To prevent any modification to the original evidence", "correct": True},
                    {"id": "d", "text": "To compress the forensic image", "correct": False}
                ]
            },
            {
                "question": "What happens if the chain of custody is broken in a legal case?",
                "answers": [
                    {"id": "a", "text": "The investigation continues as normal", "correct": False},
                    {"id": "b", "text": "The evidence may be deemed inadmissible in court", "correct": True},
                    {"id": "c", "text": "The forensic analyst is automatically fired", "correct": False},
                    {"id": "d", "text": "The case is automatically dismissed", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "threat-intelligence",
        "title": "Threat Intelligence & IOCs",
        "slug": "new-threat-intelligence",
        "description": "How organizations collect, analyze, and operationalize threat intelligence using IOCs, TTPs, and frameworks like MITRE ATT&CK.",
        "hook": "Knowing your enemy is half the battle — in cybersecurity, threat intelligence is how you learn who's attacking and how.",
        "problem": "Most security teams drown in raw indicators of compromise without understanding the context, missing the bigger picture of who is attacking and why.",
        "explanation": "Threat intelligence operates at three levels: strategic (executive decisions), operational (campaign tracking), and tactical (technical IOCs like IPs, domains, hashes). TTPs describe adversary behavior patterns while IOCs are specific artifacts. STIX/TAXII standardize sharing, and MITRE ATT&CK maps techniques to real-world behavior.",
        "real_world_example": "A SOC team received thousands of IOCs from a threat feed but couldn't prioritize. By mapping them to MITRE ATT&CK techniques and understanding the threat actor's TTPs, they identified which alerts represented actual risk versus noise, cutting false positives by 60%.",
        "summary": "Raw IOCs without context are noise. True threat intelligence combines indicators with adversary behavior, campaigns, and intent to drive actionable defense decisions.",
        "curiosity_hook": "Did you know that threat actors reuse their tools and infrastructure so predictably that you can identify them by their coding mistakes?",
        "dialogue": [
            {"speaker": "Peter", "text": "What exactly is threat intelligence? Just a list of bad IP addresses?"},
            {"speaker": "Stewie", "text": "If that were enough, we'd have solved cybersecurity. It's the collection and analysis of information about adversaries."},
            {"speaker": "Peter", "text": "What are IOCs then?"},
            {"speaker": "Stewie", "text": "Indicators of Compromise — specific artifacts like IPs, domains, file hashes that indicate malicious activity."},
            {"speaker": "Peter", "text": "So what's the problem with just blocking those IPs?"},
            {"speaker": "Stewie", "text": "Attackers rotate infrastructure constantly. IOCs expire in hours. TTPs — their tactics and procedures — are far more persistent."},
            {"speaker": "Peter", "text": "How do organizations share threat intel?"},
            {"speaker": "Stewie", "text": "STIX is the data format, TAXII is the transport. They standardize how threat intel is described and shared between teams."},
            {"speaker": "Peter", "text": "What's MITRE ATT&CK got to do with this?"},
            {"speaker": "Stewie", "text": "It maps adversary techniques to real-world behavior. When you see a technique in logs, ATT&CK tells you which groups use it."},
            {"speaker": "Peter", "text": "So context matters more than raw data?"},
            {"speaker": "Stewie", "text": "Always. A malicious IP means nothing without knowing who's behind it, what campaign it serves, and what techniques it enables."}
        ],
        "learning_objectives": [
            "Distinguish between strategic, operational, and tactical threat intelligence",
            "Understand the difference between IOCs and TTPs and why context matters more than raw indicators",
            "Explain how STIX/TAXII and MITRE ATT&CK integrate into threat intelligence programs",
            "Apply threat intelligence to proactive threat hunting workflows"
        ],
        "quiz_questions": [
            {
                "question": "Why are TTPs generally more valuable than IOCs for long-term defense?",
                "answers": [
                    {"id": "a", "text": "TTPs are always public while IOCs are private", "correct": False},
                    {"id": "b", "text": "TTPs describe adversary behavior patterns that remain consistent even as infrastructure changes", "correct": True},
                    {"id": "c", "text": "TTPs are easier to block with firewall rules", "correct": False},
                    {"id": "d", "text": "TTPs don't require any analysis to use", "correct": False}
                ]
            },
            {
                "question": "What role does TAXII play in threat intelligence sharing?",
                "answers": [
                    {"id": "a", "text": "It defines the data format for threat indicators", "correct": False},
                    {"id": "b", "text": "It's the transport protocol for sharing STIX-formatted threat intel", "correct": True},
                    {"id": "c", "text": "It automatically blocks malicious IPs at the network perimeter", "correct": False},
                    {"id": "d", "text": "It replaces the need for threat intelligence platforms", "correct": False}
                ]
            },
            {
                "question": "What is the primary benefit of mapping alerts to the MITRE ATT&CK framework?",
                "answers": [
                    {"id": "a", "text": "It automatically remediates all detected threats", "correct": False},
                    {"id": "b", "text": "It helps prioritize alerts by understanding adversary behavior and known group associations", "correct": True},
                    {"id": "c", "text": "It eliminates the need for threat intelligence feeds", "correct": False},
                    {"id": "d", "text": "It generates compliance reports for auditors", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "risk-management",
        "title": "Cybersecurity Risk Management",
        "slug": "new-risk-management",
        "description": "How organizations identify, analyze, and treat cybersecurity risks using frameworks like NIST RMF and models like FAIR.",
        "hook": "You can't protect against everything — so how do you decide what to protect first?",
        "problem": "Security teams often chase the latest threats instead of focusing on the risks that actually matter to their organization's mission and bottom line.",
        "explanation": "Risk management is the process of identifying threats and vulnerabilities, assessing their likelihood and impact, and choosing how to handle them. Qualitative analysis uses risk matrices with likelihood and impact ratings. Quantitative analysis assigns dollar values using formulas like Annual Loss Expectancy = Single Loss Expectancy x Annual Rate of Occurrence.",
        "real_world_example": "A hospital used the FAIR model to quantify ransomware risk at $4.2M annually. This justified a $500K security investment to the board — translating technical risk into financial language executives understand.",
        "summary": "Risk management isn't about eliminating all risk — it's about making informed decisions on where to invest limited resources for maximum protection of what matters most.",
        "curiosity_hook": "Did you know that the formula for Annual Loss Expectancy is simple enough to fit on a napkin, yet most organizations never calculate it?",
        "dialogue": [
            {"speaker": "Peter", "text": "Why can't we just patch everything and be done with it?"},
            {"speaker": "Stewie", "text": "Because you have infinite threats and finite resources. Risk management helps you prioritize."},
            {"speaker": "Peter", "text": "What's the difference between qualitative and quantitative analysis?"},
            {"speaker": "Stewie", "text": "Qualitative uses high-medium-low scales. Quantitative assigns dollar values — like Annual Loss Expectancy."},
            {"speaker": "Peter", "text": "How do you calculate Annual Loss Expectancy?"},
            {"speaker": "Stewie", "text": "Single Loss Expectancy times Annual Rate of Occurrence. A breach costing a million dollars once every five years is $200K ALE."},
            {"speaker": "Peter", "text": "What do you do once you know the risks?"},
            {"speaker": "Stewie", "text": "Accept it, mitigate with controls, transfer with insurance, or avoid the activity entirely. Four options."},
            {"speaker": "Peter", "text": "Is there a framework for all this?"},
            {"speaker": "Stewie", "text": "NIST RMF is the gold standard. FAIR is excellent for quantitative analysis. Both translate risk into business language."},
            {"speaker": "Peter", "text": "So risk management is a business decision, not just a technical one?"},
            {"speaker": "Stewie", "text": "Exactly. Security exists to enable the business. Risk management bridges the gap between IT and the board."}
        ],
        "learning_objectives": [
            "Explain the difference between qualitative and quantitative risk analysis",
            "Calculate Annual Loss Expectancy using Single Loss Expectancy and Annual Rate of Occurrence",
            "Understand the four risk treatment options: accept, mitigate, transfer, and avoid",
            "Apply NIST RMF and FAIR model principles to real-world security decisions"
        ],
        "quiz_questions": [
            {
                "question": "If a data breach costs $500,000 per incident and is expected to occur twice per year, what is the Annual Loss Expectancy?",
                "answers": [
                    {"id": "a", "text": "$500,000", "correct": False},
                    {"id": "b", "text": "$1,000,000", "correct": True},
                    {"id": "c", "text": "$250,000", "correct": False},
                    {"id": "d", "text": "$2,000,000", "correct": False}
                ]
            },
            {
                "question": "Which of the following is NOT one of the four risk treatment options?",
                "answers": [
                    {"id": "a", "text": "Accept", "correct": False},
                    {"id": "b", "text": "Mitigate", "correct": False},
                    {"id": "c", "text": "Ignore", "correct": True},
                    {"id": "d", "text": "Transfer", "correct": False}
                ]
            },
            {
                "question": "What is the primary advantage of quantitative risk analysis over qualitative?",
                "answers": [
                    {"id": "a", "text": "It's faster to perform", "correct": False},
                    {"id": "b", "text": "It requires less data", "correct": False},
                    {"id": "c", "text": "It translates risk into financial terms that executives can understand and act on", "correct": True},
                    {"id": "d", "text": "It eliminates subjectivity entirely", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "security-awareness",
        "title": "Security Awareness & Training",
        "slug": "new-security-awareness",
        "description": "Building a security-first culture through effective awareness programs, phishing simulations, and role-based training.",
        "hook": "You can buy the best security tools in the world, but if your employees click every phishing link, you're still compromised.",
        "problem": "Organizations treat security as a purely technical problem while ignoring the human element — resulting in training programs that check a box but don't change behavior.",
        "explanation": "Security awareness transforms employees from vulnerabilities into defenders. Effective programs use phishing simulations to measure click rates and report rates, gamification to drive engagement, and role-based training to tailor content. The goal is building a security culture, not just meeting compliance requirements.",
        "real_world_example": "Google reduced successful phishing attacks by 50% through their re:Work security awareness program, which used regular simulations, immediate feedback, and positive reinforcement rather than punishment for clicking.",
        "summary": "The human firewall is only as strong as the culture supporting it. Technical controls fail without human awareness, and awareness fails without organizational commitment.",
        "curiosity_hook": "Did you know that employees who report phishing are 4x more valuable than employees who never click — because they're actively defending the organization?",
        "dialogue": [
            {"speaker": "Peter", "text": "Why do we need security training if we have firewalls and antivirus?"},
            {"speaker": "Stewie", "text": "Because the best firewall can't stop an employee from typing their password into a fake login page."},
            {"speaker": "Peter", "text": "What are phishing simulations?"},
            {"speaker": "Stewie", "text": "You send fake phishing emails and measure who clicks, who reports, and who ignores. It's the best metric for security culture."},
            {"speaker": "Peter", "text": "What if someone fails? Do they get fired?"},
            {"speaker": "Stewie", "text": "Punishment drives hiding, not improvement. The best programs teach immediately — click the link, get instant training."},
            {"speaker": "Peter", "text": "What's the difference between compliance and culture?"},
            {"speaker": "Stewie", "text": "Compliance means you completed the module. Culture means you changed your behavior without being told to."},
            {"speaker": "Peter", "text": "How do you measure if a program is working?"},
            {"speaker": "Stewie", "text": "Track click rates and report rates over time. Click rates down and report rates up means your culture is improving."},
            {"speaker": "Peter", "text": "So the human firewall is a real concept?"},
            {"speaker": "Stewie", "text": "The most important one. Technology is the shield, but people are the first and last line of defense."}
        ],
        "learning_objectives": [
            "Understand why technical controls fail without human awareness and behavior change",
            "Design effective phishing simulation programs with meaningful metrics like click rates and report rates",
            "Differentiate between compliance-based training and genuine security culture",
            "Apply gamification and role-based training strategies to improve engagement and effectiveness"
        ],
        "quiz_questions": [
            {
                "question": "Why are employees who report phishing considered more valuable than those who never click?",
                "answers": [
                    {"id": "a", "text": "They have more technical knowledge", "correct": False},
                    {"id": "b", "text": "They actively defend the organization by identifying and reporting threats", "correct": True},
                    {"id": "c", "text": "They receive higher salaries for reporting", "correct": False},
                    {"id": "d", "text": "They are required to report by law", "correct": False}
                ]
            },
            {
                "question": "What is the key difference between security compliance and security culture?",
                "answers": [
                    {"id": "a", "text": "Compliance is voluntary, culture is mandatory", "correct": False},
                    {"id": "b", "text": "Compliance means completing required training, culture means employees naturally practice secure behaviors", "correct": True},
                    {"id": "c", "text": "Culture only applies to technology companies", "correct": False},
                    {"id": "d", "text": "Compliance is more important than culture", "correct": False}
                ]
            },
            {
                "question": "Why should organizations avoid punishing employees who fail phishing simulations?",
                "answers": [
                    {"id": "a", "text": "Punishment is illegal in most countries", "correct": False},
                    {"id": "b", "text": "Punishment drives hiding behavior rather than encouraging reporting and learning", "correct": True},
                    {"id": "c", "text": "Employees have a right to click any link they want", "correct": False},
                    {"id": "d", "text": "Punishment has no effect on security behavior", "correct": False}
                ]
            }
        ]
    }
]
