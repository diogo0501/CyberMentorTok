from dialogue_rewriter import rewrite_lessons_dialogues


LESSONS = [
    {
        "concept_slug": "app-security-arch",
        "title": "Secure Development Lifecycle (SDL)",
        "slug": "sc100-secure-development-lifecycle",
        "description": "Master the Microsoft Secure Development Lifecycle — from training and requirements through design, implementation, verification, and incident response.",
        "hook": "Every major breach traces back to a vulnerability that slipped through development. The SDL is your systematic way to catch them before they ship.",
        "problem": "Most teams bolt security on at the end of a sprint. That's like installing locks after a burglar moves in.",
        "explanation": "The SDL embeds security into every phase of software development — training, requirements, design, implementation, verification, and response. You do threat modeling at design time, security code review before merge, and fuzz testing before release.",
        "real_world_example": "Microsoft adopted SDL after the Blaster worm hit Windows XP in 2003. Since then, major vulnerabilities in Windows and Azure dropped dramatically.",
        "summary": "Security isn't a phase — it's a discipline woven through every stage of the lifecycle.",
        "curiosity_hook": "Did you know Microsoft requires every developer to complete SDL training before they can commit code to any shipping product?",
        "dialogue": [
            {"speaker": "Peter", "text": "So Stewie, what exactly is the Secure Development Lifecycle?"},
            {"speaker": "Stewie", "text": "It's Microsoft's framework for building security into software from day one."},
            {"speaker": "Peter", "text": "Can't you just test for bugs at the end?"},
            {"speaker": "Stewie", "text": "That's like checking for termites after you've bought the house. Way more expensive to fix."},
            {"speaker": "Peter", "text": "So when does security actually start?"},
            {"speaker": "Stewie", "text": "Phase one — training. Developers need to know what insecure code looks like before they write it."},
            {"speaker": "Peter", "text": "And then what?"},
            {"speaker": "Stewie", "text": "Requirements phase. You define security requirements just like functional ones. Think authentication, encryption, input validation."},
            {"speaker": "Peter", "text": "What about the design stage?"},
            {"speaker": "Stewie", "text": "That's where threat modeling lives. You analyze attack surfaces and map out trust boundaries before a single line of code."},
            {"speaker": "Peter", "text": "Does it slow down development?"},
            {"speaker": "Stewie", "text": "It slows you down a little upfront. But it saves months of patching and incident response later."}
        ],
        "learning_objectives": [
            "Identify the six phases of the Microsoft SDL and their security activities",
            "Apply threat modeling and attack surface analysis during the design phase",
            "Implement security code review and fuzz testing during verification",
            "Develop an incident response plan as part of the SDL response phase"
        ],
        "quiz_questions": [
            {
                "question": "What is the FIRST phase of the Microsoft Secure Development Lifecycle?",
                "answers": [
                    {"id": "a", "text": "Design", "correct": False},
                    {"id": "b", "text": "Training", "correct": True},
                    {"id": "c", "text": "Implementation", "correct": False},
                    {"id": "d", "text": "Verification", "correct": False}
                ]
            },
            {
                "question": "Which SDL activity should occur during the design phase?",
                "answers": [
                    {"id": "a", "text": "Fuzz testing", "correct": False},
                    {"id": "b", "text": "Security code review", "correct": False},
                    {"id": "c", "text": "Threat modeling", "correct": True},
                    {"id": "d", "text": "Incident response planning", "correct": False}
                ]
            },
            {
                "question": "Why is security testing at the end of development more expensive than shift-left?",
                "answers": [
                    {"id": "a", "text": "Tools are more expensive at that stage", "correct": False},
                    {"id": "b", "text": "Fixing vulnerabilities late requires redesign, retesting, and redeployment", "correct": True},
                    {"id": "c", "text": "Developers refuse to fix bugs after release", "correct": False},
                    {"id": "d", "text": "Compliance audits only happen at the end", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "devsecops-arch",
        "title": "DevSecOps: Shifting Security Left",
        "slug": "sc100-devsecops-shift-left",
        "description": "Learn how DevSecOps integrates automated security testing into CI/CD pipelines using GitHub Advanced Security, Azure DevOps, and shift-left principles.",
        "hook": "DevOps without security is just a fast way to ship vulnerabilities. DevSecOps bakes security into every pipeline stage.",
        "problem": "Traditional security reviews happen right before deployment, creating bottlenecks and leaving a huge window where vulnerable code sits unchecked.",
        "explanation": "DevSecOps shifts security left by automating code scanning, secret detection, and dependency analysis directly in your CI/CD pipeline. GitHub Advanced Security provides CodeQL analysis, secret scanning, and dependency reviews — all triggered on every pull request.",
        "real_world_example": "GitHub's own secret scanning has caught over a million leaked tokens since launch — from AWS keys in public repos to Azure connection strings accidentally committed.",
        "summary": "Shift-left isn't about doing less security — it's about doing security earlier, faster, and automatically.",
        "curiosity_hook": "Did you know that CodeQL can query your codebase like a database? You literally write SQL to find vulnerabilities.",
        "dialogue": [
            {"speaker": "Peter", "text": "So DevSecOps is just DevOps with security added on?"},
            {"speaker": "Stewie", "text": "No. That's DevOps with a firewall bolted on at the end. Real DevSecOps weaves security into every pipeline stage."},
            {"speaker": "Peter", "text": "How do you actually do that?"},
            {"speaker": "Stewie", "text": "Automation. Every pull request triggers code scanning, secret scanning, and dependency review automatically."},
            {"speaker": "Peter", "text": "What's CodeQL? I keep hearing about it."},
            {"speaker": "Stewie", "text": "It treats your code like a database. You write queries to find vulnerability patterns across your entire codebase."},
            {"speaker": "Peter", "text": "That sounds complicated."},
            {"speaker": "Stewie", "text": "GitHub has pre-built queries for the OWASP Top 10. You don't write them from scratch."},
            {"speaker": "Peter", "text": "What about secret scanning?"},
            {"speaker": "Stewie", "text": "It catches API keys, tokens, and connection strings before they hit your repo. Over a million leaked secrets caught so far."},
            {"speaker": "Peter", "text": "Nice. So what breaks the build?"},
            {"speaker": "Stewie", "text": "Security gates in branch policies. Critical findings block the merge. No exceptions."}
        ],
        "learning_objectives": [
            "Explain the difference between DevOps and DevSecOps",
            "Configure GitHub Advanced Security features including CodeQL, secret scanning, and dependency review",
            "Implement security gates and branch policies in CI/CD pipelines",
            "Design automated security testing workflows in Azure DevOps"
        ],
        "quiz_questions": [
            {
                "question": "What does 'shifting left' mean in DevSecOps?",
                "answers": [
                    {"id": "a", "text": "Moving security testing to production only", "correct": False},
                    {"id": "b", "text": "Integrating security earlier in the development lifecycle", "correct": True},
                    {"id": "c", "text": "Using left-handed encryption algorithms", "correct": False},
                    {"id": "d", "text": "Reducing the number of security reviews", "correct": False}
                ]
            },
            {
                "question": "What is the primary purpose of CodeQL in GitHub Advanced Security?",
                "answers": [
                    {"id": "a", "text": "Scanning for leaked secrets", "correct": False},
                    {"id": "b", "text": "Querying code as a database to find vulnerability patterns", "correct": True},
                    {"id": "c", "text": "Managing deployment secrets", "correct": False},
                    {"id": "d", "text": "Encrypting code at rest", "correct": False}
                ]
            },
            {
                "question": "How should critical security findings be handled in a DevSecOps pipeline?",
                "answers": [
                    {"id": "a", "text": "Log them and continue the build", "correct": False},
                    {"id": "b", "text": "Send an email to the security team", "correct": False},
                    {"id": "c", "text": "Block the merge with a security gate in branch policies", "correct": True},
                    {"id": "d", "text": "Wait until the next sprint to address them", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "devsecops-arch",
        "title": "Infrastructure as Code Security",
        "slug": "sc100-iac-security",
        "description": "Secure your infrastructure as code deployments with scanning tools, policy-as-code, drift detection, and secure template patterns for ARM, Bicep, and Terraform.",
        "hook": "Your ARM templates define your entire cloud footprint. One misconfigured resource can expose everything. IaC security isn't optional.",
        "problem": "Infrastructure as Code spreads security misconfigurations at scale — one bad template deploys insecure infrastructure across hundreds of environments.",
        "explanation": "IaC security involves scanning templates with tools like Checkov and Defender for Cloud before deployment, using policy-as-code to enforce standards, detecting configuration drift, and following secure patterns for secrets management and network isolation.",
        "real_world_example": "A major cloud breach in 2023 was traced back to an S3 bucket permission defined in a Terraform template that was copied across 40 environments without review.",
        "summary": "If your infrastructure is code, your code needs security reviews, scanning, and policy enforcement.",
        "curiosity_hook": "Did you know Defender for Cloud can scan your ARM templates during deployment and flag violations before resources are created?",
        "dialogue": [
            {"speaker": "Peter", "text": "Why do we need to secure infrastructure as code?"},
            {"speaker": "Stewie", "text": "Because IaC deploys at scale. One misconfiguration template can compromise an entire environment."},
            {"speaker": "Peter", "text": "Can't we just review the templates manually?"},
            {"speaker": "Stewie", "text": "You can review one. Now try reviewing 500 lines of ARM JSON without a tool. Good luck."},
            {"speaker": "Stewie", "text": "Tools like Checkov and Defender for Cloud scan your templates for misconfigurations automatically."},
            {"speaker": "Peter", "text": "What kind of misconfigurations?"},
            {"speaker": "Stewie", "text": "Open storage accounts, unrestricted network rules, missing encryption, overprivileged identities. The classics."},
            {"speaker": "Peter", "text": "What's policy-as-code?"},
            {"speaker": "Stewie", "text": "Azure Policy that runs before deployment. If your template violates a policy, it gets rejected. No exceptions."},
            {"speaker": "Peter", "text": "What about drift?"},
            {"speaker": "Stewie", "text": "Someone manually changes a resource in the portal. Drift detection catches the gap between your template and reality."},
            {"speaker": "Peter", "text": "So IaC security is basically guardrails for your cloud?"},
            {"speaker": "Stewie", "text": "Exactly. Automated guardrails that scale with your infrastructure."}
        ],
        "learning_objectives": [
            "Identify security risks in ARM, Bicep, and Terraform templates",
            "Configure Checkov and Defender for Cloud for IaC scanning",
            "Implement policy-as-code to enforce infrastructure security standards",
            "Detect and remediate configuration drift in deployed resources"
        ],
        "quiz_questions": [
            {
                "question": "What is the primary risk of IaC misconfigurations?",
                "answers": [
                    {"id": "a", "text": "Slower deployment times", "correct": False},
                    {"id": "b", "text": "Security vulnerabilities replicated at scale across environments", "correct": True},
                    {"id": "c", "text": "Higher cloud costs", "correct": False},
                    {"id": "d", "text": "Reduced code readability", "correct": False}
                ]
            },
            {
                "question": "What does configuration drift mean?",
                "answers": [
                    {"id": "a", "text": "Templates gradually change their syntax", "correct": False},
                    {"id": "b", "text": "Manual changes create gaps between deployed resources and IaC definitions", "correct": True},
                    {"id": "c", "text": "Cloud providers update their APIs", "correct": False},
                    {"id": "d", "text": "Terraform modules become outdated", "correct": False}
                ]
            },
            {
                "question": "How does policy-as-code enforce security in IaC?",
                "answers": [
                    {"id": "a", "text": "It encrypts templates before storage", "correct": False},
                    {"id": "b", "text": "It automatically fixes violations in templates", "correct": False},
                    {"id": "c", "text": "It rejects deployments that violate defined security policies", "correct": True},
                    {"id": "d", "text": "It requires manual approval for every deployment", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "app-security-arch",
        "title": "Threat Modeling with STRIDE",
        "slug": "sc100-threat-modeling-stride",
        "description": "Apply the STRIDE threat modeling methodology to systematically identify and prioritize security threats in your application architecture.",
        "hook": "Attackers don't think in terms of features — they think in terms of threats. STRIDE gives you the same lens before they exploit your system.",
        "problem": "Without a structured approach to threat identification, teams miss entire categories of vulnerabilities and waste time on unlikely scenarios.",
        "explanation": "STRIDE categorizes threats into six types: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege. By mapping these to elements in your data flow diagrams, you systematically cover every attack surface.",
        "real_world_example": "Microsoft's Threat Modeling Tool applies STRIDE to Data Flow Diagrams and has been used to secure everything from Azure services to Xbox Live.",
        "summary": "STRIDE turns 'what could go wrong?' from a vague worry into a structured, repeatable analysis.",
        "curiosity_hook": "Did you know that STRIDE was invented at Microsoft in 1999 and it's still the gold standard for threat modeling today?",
        "dialogue": [
            {"speaker": "Peter", "text": "What is STRIDE exactly?"},
            {"speaker": "Stewie", "text": "Six categories of threats. Spoofing, Tampering, Repudiation, Info Disclosure, DoS, and Elevation of Privilege."},
            {"speaker": "Peter", "text": "Can you break those down simply?"},
            {"speaker": "Stewie", "text": "Spoofing is pretending to be someone else. Tampering is modifying data. Repudiation is denying you did something."},
            {"speaker": "Stewie", "text": "Info Disclosure is leaking data. DoS is crashing the system. Elevation of Privilege is gaining unauthorized access."},
            {"speaker": "Peter", "text": "How do you actually apply this?"},
            {"speaker": "Stewie", "text": "You draw a Data Flow Diagram, identify trust boundaries, then ask STRIDE questions for each element."},
            {"speaker": "Peter", "text": "That sounds tedious."},
            {"speaker": "Stewie", "text": "Microsoft's Threat Modeling Tool automates half of it. It generates threat trees from your diagram."},
            {"speaker": "Peter", "text": "What's a threat tree?"},
            {"speaker": "Stewie", "text": "It breaks down a high-level threat into the exact steps an attacker would take. Great for prioritizing."},
            {"speaker": "Peter", "text": "How do you decide which threats matter most?"},
            {"speaker": "Stewie", "text": "Risk matrix. Likelihood times impact. Focus on what's realistic and devastating."}
        ],
        "learning_objectives": [
            "Apply all six STRIDE threat categories to application components",
            "Create and analyze Data Flow Diagrams with trust boundaries",
            "Use Microsoft Threat Modeling Tool to generate threat trees",
            "Prioritize identified threats using a risk-based approach"
        ],
        "quiz_questions": [
            {
                "question": "Which STRIDE category covers an attacker gaining admin access to a system they shouldn't have access to?",
                "answers": [
                    {"id": "a", "text": "Spoofing", "correct": False},
                    {"id": "b", "text": "Tampering", "correct": False},
                    {"id": "c", "text": "Elevation of Privilege", "correct": True},
                    {"id": "d", "text": "Information Disclosure", "correct": False}
                ]
            },
            {
                "question": "What is a trust boundary in a Data Flow Diagram?",
                "answers": [
                    {"id": "a", "text": "A firewall configuration", "correct": False},
                    {"id": "b", "text": "A line where the level of trust changes between components", "correct": True},
                    {"id": "c", "text": "An encrypted connection", "correct": False},
                    {"id": "d", "text": "A user authentication point", "correct": False}
                ]
            },
            {
                "question": "What should you prioritize when evaluating identified threats?",
                "answers": [
                    {"id": "a", "text": "The threats that are easiest to demonstrate", "correct": False},
                    {"id": "b", "text": "Threats with the highest likelihood and impact combination", "correct": True},
                    {"id": "c", "text": "Threats identified by the automated tool only", "correct": False},
                    {"id": "d", "text": "Threats that affect third-party dependencies", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "app-security-arch",
        "title": "API Security",
        "slug": "sc100-api-security",
        "description": "Secure your APIs with Azure API Management, OAuth 2.0, rate limiting, and protection against the OWASP API Security Top 10 threats.",
        "hook": "APIs are the front door to every modern application. If you secure the web app but not its API, you've locked the window and left the door wide open.",
        "problem": "APIs expose business logic directly to consumers. Unlike UIs, they don't have built-in browser protections, making them prime targets for mass data extraction and abuse.",
        "explanation": "API security combines authentication with OAuth 2.0 and JWT tokens, Azure API Management for rate limiting and throttling, and defense against the OWASP API Security Top 10 including broken object level authorization, excessive data exposure, and injection attacks.",
        "real_world_example": "The T-Mobile API breach in 2023 exposed data of 37 million customers through an API vulnerability — no authentication bypass needed, just an insecure API endpoint.",
        "summary": "APIs need their own security layer. Your app's authentication doesn't automatically protect its endpoints.",
        "curiosity_hook": "Did you know that the OWASP API Security Top 10 is completely different from the web application Top 10? APIs have their own threat landscape.",
        "dialogue": [
            {"speaker": "Peter", "text": "Why is API security different from web app security?"},
            {"speaker": "Stewie", "text": "APIs are machine-to-machine. There's no browser, no CSRF protection, no same-origin policy. You're naked."},
            {"speaker": "Peter", "text": "Naked? That's alarming."},
            {"speaker": "Stewie", "text": "APIs expose raw business logic. An attacker can call endpoints directly and skip your entire UI validation layer."},
            {"speaker": "Peter", "text": "How do you secure them?"},
            {"speaker": "Stewie", "text": "OAuth 2.0 for authentication, JWT tokens for authorization, and Azure API Management for rate limiting."},
            {"speaker": "Peter", "text": "What's broken object level authorization?"},
            {"speaker": "Stewie", "text": "It's when you can access any user's data just by changing an ID in the URL. /api/users/123 becomes /api/users/124. Classic."},
            {"speaker": "Peter", "text": "That sounds way too easy to exploit."},
            {"speaker": "Stewie", "text": "It's the number one API vulnerability for a reason. Simple but devastating."},
            {"speaker": "Peter", "text": "What about rate limiting?"},
            {"speaker": "Stewie", "text": "Without it, attackers hammer your API with thousands of requests per second. API Management throttles that abuse."}
        ],
        "learning_objectives": [
            "Implement OAuth 2.0 and JWT-based authentication for APIs",
            "Configure Azure API Management rate limiting and throttling policies",
            "Identify and mitigate threats from the OWASP API Security Top 10",
            "Design API gateway patterns for centralized security enforcement"
        ],
        "quiz_questions": [
            {
                "question": "What is the most common API security vulnerability according to OWASP?",
                "answers": [
                    {"id": "a", "text": "SQL injection", "correct": False},
                    {"id": "b", "text": "Broken Object Level Authorization", "correct": True},
                    {"id": "c", "text": "Cross-site scripting", "correct": False},
                    {"id": "d", "text": "Denial of service", "correct": False}
                ]
            },
            {
                "question": "What role does Azure API Management play in API security?",
                "answers": [
                    {"id": "a", "text": "It replaces the need for authentication", "correct": False},
                    {"id": "b", "text": "It provides rate limiting, throttling, and centralized security policies", "correct": True},
                    {"id": "c", "text": "It encrypts API responses end-to-end", "correct": False},
                    {"id": "d", "text": "It generates API documentation only", "correct": False}
                ]
            },
            {
                "question": "Why is OAuth 2.0 preferred over API keys for API authentication?",
                "answers": [
                    {"id": "a", "text": "API keys are always public", "correct": False},
                    {"id": "b", "text": "OAuth provides token-based access with scopes and expiration, not just a static key", "correct": True},
                    {"id": "c", "text": "OAuth doesn't require any configuration", "correct": False},
                    {"id": "d", "text": "API keys cannot be transmitted over HTTPS", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "cloud-frameworks",
        "title": "Web Application Firewall (WAF)",
        "slug": "sc100-web-application-firewall",
        "description": "Deploy and configure Azure WAF with Application Gateway and Front Door to protect web applications from OWASP threats, bots, and DDoS attacks.",
        "hook": "A WAF is your application's bouncer. It checks every request at the door and throws out the suspicious ones before they reach your code.",
        "problem": "Web applications face constant automated attacks — SQL injection, XSS, credential stuffing, and bot traffic. Without a WAF, your application absorbs all of it.",
        "explanation": "Azure WAF integrates with Application Gateway and Azure Front Door to inspect HTTP traffic using managed rule sets like OWASP CRS and Microsoft Bot Manager. It supports custom rules, geo-filtering, rate limiting, and runs in detection or prevention mode.",
        "real_world_example": "Azure Front Door with WAF blocked over 100 billion malicious requests in 2023 alone, protecting customers from automated exploitation attempts.",
        "summary": "A WAF doesn't replace secure coding — it provides defense in depth when your application faces the public internet.",
        "curiosity_hook": "Did you know attackers use techniques like Unicode normalization and HTTP parameter pollution to evade WAF rules? That's why rule updates matter.",
        "dialogue": [
            {"speaker": "Peter", "text": "Do I really need a WAF if my app has input validation?"},
            {"speaker": "Stewie", "text": "Input validation is great. A WAF catches what slips through. Defense in depth, Peter."},
            {"speaker": "Peter", "text": "What's the difference between Application Gateway WAF and Front Door WAF?"},
            {"speaker": "Stewie", "text": "Application Gateway is regional. Front Door is global. Both run the same WAF engine and rule sets."},
            {"speaker": "Peter", "text": "What do the OWASP rules actually block?"},
            {"speaker": "Stewie", "text": "SQL injection, XSS, path traversal, remote code execution. The OWASP Core Rule Set covers the classics."},
            {"speaker": "Peter", "text": "Detection or prevention mode — which should I use?"},
            {"speaker": "Stewie", "text": "Start with detection to avoid breaking legitimate traffic. Then switch to prevention once you've tuned your rules."},
            {"speaker": "Peter", "text": "Can attackers get around a WAF?"},
            {"speaker": "Stewie", "text": "Sure. Unicode tricks, encoding bypasses, slow-rate attacks. That's why you need custom rules and regular updates."},
            {"speaker": "Peter", "text": "Sounds like an arms race."},
            {"speaker": "Stewie", "text": "That's cybersecurity in a nutshell. The WAF gives you the high ground."}
        ],
        "learning_objectives": [
            "Configure Azure WAF with Application Gateway and Azure Front Door",
            "Apply OWASP CRS and Microsoft managed rule sets for threat protection",
            "Create custom WAF rules for application-specific protection",
            "Implement detection and prevention modes with proper tuning"
        ],
        "quiz_questions": [
            {
                "question": "What is the difference between WAF detection and prevention mode?",
                "answers": [
                    {"id": "a", "text": "Detection blocks traffic; prevention logs only", "correct": False},
                    {"id": "b", "text": "Detection logs threats without blocking; prevention actively blocks malicious requests", "correct": True},
                    {"id": "c", "text": "They are functionally identical", "correct": False},
                    {"id": "d", "text": "Detection is for production; prevention is for testing", "correct": False}
                ]
            },
            {
                "question": "Which Azure service provides global WAF protection with edge-based rule evaluation?",
                "answers": [
                    {"id": "a", "text": "Azure Application Gateway", "correct": False},
                    {"id": "b", "text": "Azure Front Door", "correct": True},
                    {"id": "c", "text": "Azure Load Balancer", "correct": False},
                    {"id": "d", "text": "Azure Traffic Manager", "correct": False}
                ]
            },
            {
                "question": "What is the OWASP Core Rule Set primarily designed to protect against?",
                "answers": [
                    {"id": "a", "text": "DDoS attacks only", "correct": False},
                    {"id": "b", "text": "Bot traffic and credential stuffing", "correct": False},
                    {"id": "c", "text": "SQL injection, XSS, and other common web application attacks", "correct": True},
                    {"id": "d", "text": "SSL/TLS certificate issues", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "cloud-frameworks",
        "title": "DDoS Protection & Azure Network Security",
        "slug": "sc100-ddos-network-security",
        "description": "Understand Azure DDoS Protection, Private Link, Azure Firewall, and network security patterns for building resilient cloud architectures.",
        "hook": "A single DDoS attack can take down your entire service in minutes. Azure DDoS Protection gives you enterprise-grade defense that your ISP never could.",
        "problem": "DDoS attacks are cheap to launch but expensive to recover from. Without protection, even a small volumetric attack can exhaust your resources and incur massive costs.",
        "explanation": "Azure DDoS Protection Standard provides ML-based adaptive tuning, attack analytics, and cost protection. Combined with Private Link for private connectivity, Azure Firewall for network filtering, and hub-spoke topology for traffic segmentation, you get layered network defense.",
        "real_world_example": "In 2020, Azure DDoS Protection mitigated a 2.4 Tbps attack — one of the largest ever recorded — protecting customer services without manual intervention.",
        "summary": "Network security is your perimeter defense. DDoS protection, private connectivity, and firewall filtering work together to keep attacks out.",
        "curiosity_hook": "Did you know Azure DDoS Protection Standard can automatically scale mitigation capacity to absorb attacks that would overwhelm any single data center?",
        "dialogue": [
            {"speaker": "Peter", "text": "What's the difference between DDoS Basic and Standard?"},
            {"speaker": "Stewie", "text": "Basic is free and covers platform-level protection. Standard adds ML-based tuning, attack analytics, and cost protection."},
            {"speaker": "Peter", "text": "Cost protection? They pay you back?"},
            {"speaker": "Stewie", "text": "If an attack causes resource scaling, Azure credits the overage. That's how confident they are in Standard."},
            {"speaker": "Peter", "text": "What about Private Link?"},
            {"speaker": "Stewie", "text": "It gives your services private IP addresses across the Microsoft backbone. Traffic never touches the public internet."},
            {"speaker": "Peter", "text": "So it's like a private tunnel?"},
            {"speaker": "Stewie", "text": "Exactly. No public exposure, no attack surface, no data traversing the open web."},
            {"speaker": "Peter", "text": "Where does Azure Firewall fit in?"},
            {"speaker": "Stewie", "text": "It filters east-west and north-south traffic. Premium adds TLS inspection and IDPS for deep packet analysis."},
            {"speaker": "Peter", "text": "Hub-spoke topology — is that complex?"},
            {"speaker": "Stewie", "text": "It's a hub VNet with shared services like firewalls, and spoke VNets peered to it. Clean segmentation."}
        ],
        "learning_objectives": [
            "Differentiate between Azure DDoS Protection Basic and Standard features",
            "Implement Azure Private Link for private service connectivity",
            "Configure Azure Firewall for network traffic filtering and inspection",
            "Design hub-spoke and Virtual WAN topologies for network segmentation"
        ],
        "quiz_questions": [
            {
                "question": "What benefit does Azure DDoS Protection Standard provide over Basic?",
                "answers": [
                    {"id": "a", "text": "Faster internet connectivity", "correct": False},
                    {"id": "b", "text": "ML-based adaptive tuning, attack analytics, and cost protection", "correct": True},
                    {"id": "c", "text": "Higher bandwidth limits for VMs", "correct": False},
                    {"id": "d", "text": "Automatic VM migration during attacks", "correct": False}
                ]
            },
            {
                "question": "What is the primary purpose of Azure Private Link?",
                "answers": [
                    {"id": "a", "text": "To increase public bandwidth", "correct": False},
                    {"id": "b", "text": "To provide private connectivity to services over the Microsoft backbone without public internet exposure", "correct": True},
                    {"id": "c", "text": "To replace Azure Firewall", "correct": False},
                    {"id": "d", "text": "To encrypt data at rest", "correct": False}
                ]
            },
            {
                "question": "In a hub-spoke network topology, what typically resides in the hub VNet?",
                "answers": [
                    {"id": "a", "text": "Application workloads only", "correct": False},
                    {"id": "b", "text": "Shared services like firewalls, VPN gateways, and DNS", "correct": True},
                    {"id": "c", "text": "User-facing web applications", "correct": False},
                    {"id": "d", "text": "Backup and disaster recovery resources only", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "data-security",
        "title": "Azure Key Vault & Secrets Management",
        "slug": "sc100-key-vault-secrets",
        "description": "Master Azure Key Vault for managing keys, secrets, and certificates with RBAC, soft delete, purge protection, and managed identity integration.",
        "hook": "Hardcoded secrets are the number one cause of cloud breaches. Key Vault is your central nervous system for managing every secret in your organization.",
        "problem": "Secrets scattered across config files, environment variables, and source code create an impossible-to-audit attack surface. One leaked credential can compromise an entire tenant.",
        "explanation": "Key Vault centralizes keys, secrets, and certificates with fine-grained RBAC, soft delete with purge protection, private endpoints, and managed identity integration. Managed HSM provides FIPS 140-2 Level 3 isolation for the most sensitive workloads.",
        "real_world_example": "In 2024, a major SaaS company exposed over 10,000 API keys in public GitHub repos because developers hardcoded them instead of using Key Vault.",
        "summary": "Never hardcode secrets. Store them centrally in Key Vault, rotate them regularly, and access them via managed identities.",
        "curiosity_hook": "Did you know Key Vault supports envelope encryption — your data is encrypted with a DEK, and the DEK is encrypted with a KEK stored in Key Vault?",
        "dialogue": [
            {"speaker": "Peter", "text": "What's the difference between Key Vault and Managed HSM?"},
            {"speaker": "Stewie", "text": "Key Vault is multi-tenant. Managed HSM is single-tenant, FIPS 140-2 Level 3. Use HSM for highly regulated workloads."},
            {"speaker": "Peter", "text": "Why can't I just store secrets in environment variables?"},
            {"speaker": "Stewie", "text": "Because they end up in logs, config dumps, Docker images, and error reports. Secrets in env vars aren't secrets."},
            {"speaker": "Peter", "text": "Fair point. What about access control?"},
            {"speaker": "Stewie", "text": "Key Vault supports RBAC now, not just access policies. Assign roles at the vault, key, secret, or certificate level."},
            {"speaker": "Peter", "text": "What's soft delete and purge protection?"},
            {"speaker": "Stewie", "text": "Soft delete keeps deleted items for recovery. Purge protection prevents permanent deletion during the retention period. Anti-ransomware for secrets."},
            {"speaker": "Peter", "text": "How do applications access Key Vault?"},
            {"speaker": "Stewie", "text": "Managed identities. No connection strings, no secrets in code. The app authenticates to Entra ID automatically."},
            {"speaker": "Peter", "text": "That's clean. What about key rotation?"},
            {"speaker": "Stewie", "text": "Set an expiry policy. Key Vault can auto-rotate keys and secrets on a schedule."}
        ],
        "learning_objectives": [
            "Differentiate between Key Vault and Managed HSM for various security requirements",
            "Configure RBAC, soft delete, and purge protection for Key Vault resources",
            "Implement managed identities for secure Key Vault access from applications",
            "Design key and secret rotation policies for automated credential lifecycle management"
        ],
        "quiz_questions": [
            {
                "question": "What is the primary advantage of Managed HSM over standard Key Vault?",
                "answers": [
                    {"id": "a", "text": "Lower cost per transaction", "correct": False},
                    {"id": "b", "text": "FIPS 140-2 Level 3 single-tenant hardware isolation", "correct": True},
                    {"id": "c", "text": "More built-in secret types", "correct": False},
                    {"id": "d", "text": "Faster key creation", "correct": False}
                ]
            },
            {
                "question": "Why should applications use managed identities instead of connection strings to access Key Vault?",
                "answers": [
                    {"id": "a", "text": "Managed identities are faster", "correct": False},
                    {"id": "b", "text": "Managed identities eliminate secrets from code and configuration", "correct": True},
                    {"id": "c", "text": "Connection strings don't work with Key Vault", "correct": False},
                    {"id": "d", "text": "Managed identities support more encryption algorithms", "correct": False}
                ]
            },
            {
                "question": "What is the purpose of purge protection in Key Vault?",
                "answers": [
                    {"id": "a", "text": "To permanently delete secrets immediately", "correct": False},
                    {"id": "b", "text": "To prevent permanent deletion of secrets during a retention period", "correct": True},
                    {"id": "c", "text": "To encrypt secrets before storage", "correct": False},
                    {"id": "d", "text": "To back up secrets to another region", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "data-security",
        "title": "Data Encryption End-to-End",
        "slug": "sc100-data-encryption",
        "description": "Implement comprehensive data encryption across Azure — at rest, in transit, and end-to-end with customer-managed keys and confidential computing.",
        "hook": "Encryption at rest and in transit are table stakes. True data security means controlling the keys and understanding where your data is decrypted.",
        "problem": "Most organizations assume 'encrypted' means secure. But encryption without proper key management, access control, and transit protection is just theater.",
        "explanation": "Azure provides encryption at rest with Storage Service Encryption and Azure Disk Encryption, in transit with TLS 1.2, and end-to-end with Customer Managed Keys stored in Key Vault. Confidential Computing encrypts data even during processing in memory.",
        "real_world_example": "Azure Confidential Computing uses AMD SEV-SNP and Intel TDX hardware to encrypt data in use — meaning even Azure operators can't access your data during processing.",
        "summary": "Encrypt at rest, encrypt in transit, control your keys, and for the most sensitive workloads — encrypt during processing too.",
        "curiosity_hook": "Did you know AES-256 is used by the US government to protect classified information? Azure uses it as the default for storage encryption.",
        "dialogue": [
            {"speaker": "Peter", "text": "Azure encrypts everything by default, right? So why worry?"},
            {"speaker": "Stewie", "text": "Default encryption uses platform-managed keys. CMK means YOU control the keys. Big difference in compliance and control."},
            {"speaker": "Peter", "text": "What's the difference between PMK and CMK?"},
            {"speaker": "Stewie", "text": "PMK — Azure manages keys, you get encryption. CMK — you bring your own key from Key Vault. You decide when it rotates or gets revoked."},
            {"speaker": "Peter", "text": "And double encryption?"},
            {"speaker": "Stewie", "text": "Two layers of encryption with different algorithms. Even if one is compromised, the other still protects your data."},
            {"speaker": "Peter", "text": "What about data in transit?"},
            {"speaker": "Stewie", "text": "TLS 1.2 minimum. Azure enforces it across all services. No more unencrypted traffic between components."},
            {"speaker": "Peter", "text": "What's Confidential Computing?"},
            {"speaker": "Stewie", "text": "It encrypts data while it's being processed in CPU memory. Even the cloud provider can't see it."},
            {"speaker": "Peter", "text": "That sounds like magic."},
            {"speaker": "Stewie", "text": "It's hardware-level encryption using AMD SEV-SNP. Microsoft, Google, and Oracle all offer it now."}
        ],
        "learning_objectives": [
            "Implement encryption at rest using Storage Service Encryption and Azure Disk Encryption",
            "Configure Customer Managed Keys with Key Vault for data encryption control",
            "Explain Confidential Computing and its role in protecting data during processing",
            "Differentiate between platform-managed and customer-managed encryption key strategies"
        ],
        "quiz_questions": [
            {
                "question": "What does Customer Managed Keys (CMK) provide that Platform Managed Keys (PMK) do not?",
                "answers": [
                    {"id": "a", "text": "Faster encryption performance", "correct": False},
                    {"id": "b", "text": "Full control over key rotation, revocation, and lifecycle management", "correct": True},
                    {"id": "c", "text": "Encryption in transit", "correct": False},
                    {"id": "d", "text": "Automatic backup of encrypted data", "correct": False}
                ]
            },
            {
                "question": "What is the primary benefit of Azure Confidential Computing?",
                "answers": [
                    {"id": "a", "text": "Faster data processing", "correct": False},
                    {"id": "b", "text": "Encrypting data at rest and in transit", "correct": False},
                    {"id": "c", "text": "Encrypting data during processing in CPU memory", "correct": True},
                    {"id": "d", "text": "Reducing storage costs", "correct": False}
                ]
            },
            {
                "question": "What is double encryption in Azure?",
                "answers": [
                    {"id": "a", "text": "Running the same encryption algorithm twice", "correct": False},
                    {"id": "b", "text": "Two layers of encryption using different algorithms or key providers", "correct": True},
                    {"id": "c", "text": "Encrypting data only at rest and in transit", "correct": False},
                    {"id": "d", "text": "Using both AES and RSA for the same key", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "data-security",
        "title": "Data Loss Prevention (DLP)",
        "slug": "sc100-data-loss-prevention",
        "description": "Deploy Microsoft Purview DLP policies to protect sensitive data across endpoints, email, SharePoint, OneDrive, Teams, and Copilot interactions.",
        "hook": "Your employees send sensitive data every day — in emails, chats, and documents. DLP is your safety net that catches data before it leaves the organization.",
        "problem": "Sensitive data like credit card numbers, health records, and intellectual property leaks through everyday activities — a pasted SSN in Teams, a customer list shared externally, a report uploaded to personal cloud storage.",
        "explanation": "Microsoft Purview DLP policies scan content across endpoints, Exchange Online, SharePoint, OneDrive, and Teams using sensitive info types, exact data match, and trainable classifiers. Policy tips educate users, while incident reports help security teams tune policies.",
        "real_world_example": "Microsoft's own DLP policies detect over 50 billion sensitive information matches per month across Office 365 — preventing accidental leaks of PII and financial data.",
        "summary": "DLP isn't just blocking — it's educating users, detecting leaks, and providing visibility into where sensitive data flows.",
        "curiosity_hook": "Did you know DLP now covers Copilot? It can detect when AI-generated responses contain sensitive data and block the interaction.",
        "dialogue": [
            {"speaker": "Peter", "text": "How does DLP actually know what's sensitive?"},
            {"speaker": "Stewie", "text": "It uses sensitive info types — patterns like credit card numbers, SSNs, and custom formats you define."},
            {"speaker": "Peter", "text": "What about exact data match?"},
            {"speaker": "Stewie", "text": "EDM lets you hash and index your actual sensitive data. DLP checks content against the index with high precision and low false positives."},
            {"speaker": "Peter", "text": "Where does DLP work?"},
            {"speaker": "Stewie", "text": "Endpoints, Exchange, SharePoint, OneDrive, Teams. All covered by unified policies in Microsoft Purview."},
            {"speaker": "Peter", "text": "What happens when DLP detects something?"},
            {"speaker": "Stewie", "text": "Policy tips educate the user. Admins get incident reports. You can block, warn, or just log the activity."},
            {"speaker": "Peter", "text": "What about false positives?"},
            {"speaker": "Stewie", "text": "Tune your rules, use trainable classifiers, and review incident reports. It's an iterative process."},
            {"speaker": "Peter", "text": "DLP for Copilot — really?"},
            {"speaker": "Stewie", "text": "Yes. If Copilot tries to surface sensitive data in a response, DLP blocks it. Even AI needs guardrails."}
        ],
        "learning_objectives": [
            "Configure Microsoft Purview DLP policies for endpoints, email, and cloud storage",
            "Implement sensitive info types, exact data match, and trainable classifiers",
            "Analyze DLP incident reports and tune policies to reduce false positives",
            "Explain how DLP integrates with Copilot for AI-specific data protection"
        ],
        "quiz_questions": [
            {
                "question": "What is Exact Data Match (EDM) in Microsoft Purview DLP?",
                "answers": [
                    {"id": "a", "text": "Matching content against generic pattern libraries", "correct": False},
                    {"id": "b", "text": "Hashing and indexing your actual sensitive data for high-precision matching", "correct": True},
                    {"id": "c", "text": "Manually reviewing every document for sensitive data", "correct": False},
                    {"id": "d", "text": "Encrypting all data to prevent loss", "correct": False}
                ]
            },
            {
                "question": "Which services are covered by Microsoft Purview DLP policies?",
                "answers": [
                    {"id": "a", "text": "Exchange Online and SharePoint only", "correct": False},
                    {"id": "b", "text": "Endpoints, Exchange Online, SharePoint, OneDrive, Teams, and Copilot", "correct": True},
                    {"id": "c", "text": "Only on-premises file servers", "correct": False},
                    {"id": "d", "text": "Third-party cloud services only", "correct": False}
                ]
            },
            {
                "question": "What is the role of policy tips in DLP?",
                "answers": [
                    {"id": "a", "text": "They automatically delete sensitive content", "correct": False},
                    {"id": "b", "text": "They educate users about policy violations at the time of the action", "correct": True},
                    {"id": "c", "text": "They encrypt the content before sending", "correct": False},
                    {"id": "d", "text": "They notify external parties about data sharing", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "data-security",
        "title": "Data Governance with Microsoft Purview",
        "slug": "sc100-data-governance-purview",
        "description": "Build a comprehensive data governance strategy with Microsoft Purview — data mapping, classification, lineage, lifecycle management, and information protection.",
        "hook": "You can't protect data you can't find. Purview maps your entire data estate and gives you the governance controls to manage it end to end.",
        "problem": "Organizations store petabytes of data across hundreds of systems with no unified view of what exists, where it's classified, who owns it, and how long it should be retained.",
        "explanation": "Microsoft Purview provides automated data mapping and classification, a searchable data catalog, data lineage tracking, information protection with sensitivity labels, and data lifecycle management with retention policies — all in one unified platform.",
        "real_world_example": "A Fortune 500 company used Purview to discover they had 12 copies of the same customer database across 4 regions — eliminating duplicates saved them $2M in annual storage costs.",
        "summary": "Data governance turns chaotic data sprawl into an organized, classified, and managed data estate with clear ownership and lifecycle policies.",
        "curiosity_hook": "Did you know Purview's auto-classification can identify and label over 200 sensitive information types across your entire data estate automatically?",
        "dialogue": [
            {"speaker": "Peter", "text": "What is Microsoft Purview exactly?"},
            {"speaker": "Stewie", "text": "It's your data governance platform. It scans, classifies, catalogs, and tracks lineage across your entire data estate."},
            {"speaker": "Peter", "text": "How does the data map work?"},
            {"speaker": "Stewie", "text": "Auto-scan sources across on-prem, multi-cloud, and SaaS. Builds a map of every asset, classification, and relationship."},
            {"speaker": "Peter", "text": "What are sensitivity labels?"},
            {"speaker": "Stewie", "text": "Labels like Public, Internal, Confidential. You can auto-apply them based on content, and they encrypt and restrict access."},
            {"speaker": "Peter", "text": "Data lifecycle management — what does that mean?"},
            {"speaker": "Stewie", "text": "Retention labels that auto-delete or archive data based on policy. No more hoarding data forever because nobody knows what to do with it."},
            {"speaker": "Peter", "text": "What's data lineage?"},
            {"speaker": "Stewie", "text": "It tracks where data comes from and how it transforms. Critical for compliance — you can prove exactly how a report was generated."},
            {"speaker": "Peter", "text": "That sounds incredibly useful for audits."},
            {"speaker": "Stewie", "text": "That's the point. Auditors love Purview because it answers their questions automatically."}
        ],
        "learning_objectives": [
            "Configure Purview Data Map with automated scanning and classification",
            "Implement sensitivity labels for information protection and encryption",
            "Design data lifecycle management policies with retention and deletion rules",
            "Use data lineage to track data flow across sources for compliance"
        ],
        "quiz_questions": [
            {
                "question": "What is the primary purpose of the Purview Data Map?",
                "answers": [
                    {"id": "a", "text": "Storing encrypted data backups", "correct": False},
                    {"id": "b", "text": "Automatically scanning and cataloging data assets across the entire data estate", "correct": True},
                    {"id": "c", "text": "Replacing Azure Data Factory for ETL", "correct": False},
                    {"id": "d", "text": "Managing user access to applications", "correct": False}
                ]
            },
            {
                "question": "What do sensitivity labels provide in Microsoft Purview?",
                "answers": [
                    {"id": "a", "text": "Data compression for storage savings", "correct": False},
                    {"id": "b", "text": "Classification, encryption, and access restrictions based on data sensitivity", "correct": True},
                    {"id": "c", "text": "Automatic data backup scheduling", "correct": False},
                    {"id": "d", "text": "Real-time threat detection for data breaches", "correct": False}
                ]
            },
            {
                "question": "Why is data lineage important for compliance?",
                "answers": [
                    {"id": "a", "text": "It reduces storage costs", "correct": False},
                    {"id": "b", "text": "It tracks data origins and transformations, proving how reports and analytics are generated", "correct": True},
                    {"id": "c", "text": "It automatically encrypts all data flows", "correct": False},
                    {"id": "d", "text": "It replaces the need for data classification", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "workload-identity",
        "title": "Workload Identity Security",
        "slug": "sc100-workload-identity-security",
        "description": "Secure workload identities with managed identities, federated credentials, and Entra Workload ID to eliminate secrets from applications and pipelines.",
        "hook": "Every leaked secret in your codebase is a ticking bomb. Workload identities let your applications authenticate without ever touching a single credential.",
        "problem": "Applications, services, and CI/CD pipelines still authenticate using hardcoded secrets and certificates — creating massive credential sprawl and breach risk.",
        "explanation": "Managed identities (system and user-assigned) provide Azure resources with automatic Entra ID credentials. Workload identity federation extends this to external platforms like GitHub Actions and Kubernetes using OIDC, eliminating secrets entirely.",
        "real_world_example": "GitHub Actions OIDC federation with Azure lets workflows authenticate to Azure without storing any secrets — over 10,000 repositories have already adopted this pattern.",
        "summary": "Stop managing secrets for your applications. Use managed identities and federated credentials to authenticate without credentials.",
        "curiosity_hook": "Did you know Entra Workload ID can apply Conditional Access policies to workload identities — the same way you protect user accounts?",
        "dialogue": [
            {"speaker": "Peter", "text": "What's a workload identity exactly?"},
            {"speaker": "Stewie", "text": "It's an identity for an application or service instead of a user. Your code gets its own Entra ID identity."},
            {"speaker": "Peter", "text": "What's the difference between system and user-assigned managed identities?"},
            {"speaker": "Stewie", "text": "System-assigned is tied to one resource — delete the resource, identity goes away. User-assigned is independent, reusable across resources."},
            {"speaker": "Peter", "text": "What about federated credentials?"},
            {"speaker": "Stewie", "text": "OIDC federation lets GitHub Actions, Azure DevOps, or Kubernetes authenticate to Azure without storing any secrets."},
            {"speaker": "Peter", "text": "How does that work?"},
            {"speaker": "Stewie", "text": "The external platform issues a signed token. Azure validates the token against a trust relationship. No secret needed."},
            {"speaker": "Peter", "text": "Can I use Conditional Access on workload identities?"},
            {"speaker": "Stewie", "text": "Yes! Entra Workload ID supports Conditional Access. Restrict which networks, apps, or conditions a workload can authenticate from."},
            {"speaker": "Peter", "text": "That's powerful. Any gotchas?"},
            {"speaker": "Stewie", "text": "Federated credentials require proper trust configuration. Misconfigure the issuer URL and authentication breaks silently."}
        ],
        "learning_objectives": [
            "Differentiate between system-assigned and user-assigned managed identities",
            "Configure workload identity federation for GitHub Actions and Azure DevOps",
            "Implement Entra Workload ID with Conditional Access policies for workload identities",
            "Eliminate hardcoded secrets by transitioning to managed identity-based authentication"
        ],
        "quiz_questions": [
            {
                "question": "What is the key advantage of user-assigned managed identities over system-assigned?",
                "answers": [
                    {"id": "a", "text": "They are automatically created with the resource", "correct": False},
                    {"id": "b", "text": "They are independent of resources and can be shared across multiple workloads", "correct": True},
                    {"id": "c", "text": "They support more authentication protocols", "correct": False},
                    {"id": "d", "text": "They don't require Entra ID", "correct": False}
                ]
            },
            {
                "question": "How does OIDC federation eliminate secrets for CI/CD pipelines?",
                "answers": [
                    {"id": "a", "text": "It stores secrets in an encrypted vault", "correct": False},
                    {"id": "b", "text": "The external platform issues a signed token that Azure validates against a trust relationship", "correct": True},
                    {"id": "c", "text": "It encrypts secrets at the pipeline level", "correct": False},
                    {"id": "d", "text": "It generates rotating passwords automatically", "correct": False}
                ]
            },
            {
                "question": "What can Entra Workload ID Conditional Access restrict?",
                "answers": [
                    {"id": "a", "text": "Only user login locations", "correct": False},
                    {"id": "b", "text": "The networks, applications, and conditions under which workloads can authenticate", "correct": True},
                    {"id": "c", "text": "Only the time of day for authentication", "correct": False},
                    {"id": "d", "text": "Nothing — Conditional Access is for users only", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "ai-security",
        "title": "AI Security & Governance",
        "slug": "sc100-ai-security-governance",
        "description": "Secure AI deployments with Microsoft Purview AI hub, Defender for AI, OWASP Top 10 for LLMs, MITRE ATLAS, and responsible AI governance.",
        "hook": "AI introduces an entirely new attack surface. Prompt injection, data poisoning, and model theft aren't theoretical — they're happening right now.",
        "problem": "Organizations are deploying LLMs and AI models without understanding the unique security risks — from prompt injection that bypasses safety controls to training data poisoning that corrupts model behavior.",
        "explanation": "AI security covers the OWASP Top 10 for LLMs including prompt injection, insecure output handling, and training data poisoning. Microsoft's stack includes Purview AI hub for governance, Defender for AI for threat detection, and Prompt Shields for LLM-specific protection.",
        "real_world_example": "In 2024, researchers demonstrated prompt injection attacks that tricked banking chatbots into revealing internal system prompts and customer data — a real-world OWASP LLM Top 10 vulnerability.",
        "summary": "AI needs its own security framework. Traditional controls don't cover prompt injection, model poisoning, or excessive AI agency.",
        "curiosity_hook": "Did you know MITRE ATLAS maps real-world AI attacks against tactics and techniques similar to the ATT&CK framework — specifically for AI systems?",
        "dialogue": [
            {"speaker": "Peter", "text": "AI security — is that just regular security for AI?"},
            {"speaker": "Stewie", "text": "No. LLMs have unique attack vectors. Prompt injection, data poisoning, model theft. Traditional security doesn't cover these."},
            {"speaker": "Peter", "text": "Prompt injection? Like SQL injection?"},
            {"speaker": "Stewie", "text": "Same concept, different target. You craft input that makes the AI ignore its instructions and do what you want instead."},
            {"speaker": "Peter", "text": "That's terrifying. What about training data poisoning?"},
            {"speaker": "Stewie", "text": "Attackers corrupt the training data to make the model produce biased or malicious outputs. Like teaching a kid with a corrupted textbook."},
            {"speaker": "Peter", "text": "What's Microsoft Purview AI hub?"},
            {"speaker": "Stewie", "text": "It's governance for AI. Track which models exist, who uses them, what data they access, and ensure compliance."},
            {"speaker": "Peter", "text": "What are Prompt Shields?"},
            {"speaker": "Stewie", "text": "They detect and block prompt injection attacks against LLMs. Microsoft's answer to the OWASP LLM Top 10."},
            {"speaker": "Peter", "text": "What's MITRE ATLAS?"},
            {"speaker": "Stewie", "text": "It maps real-world AI attacks to tactics and techniques. Like ATT&CK but specifically for AI and ML systems."}
        ],
        "learning_objectives": [
            "Identify threats from the OWASP Top 10 for LLMs including prompt injection and data poisoning",
            "Configure Microsoft Purview AI hub for AI governance and compliance",
            "Explain how Microsoft Defender for AI detects threats to AI workloads",
            "Apply MITRE ATLAS framework to assess and defend against AI-specific attack techniques"
        ],
        "quiz_questions": [
            {
                "question": "What is prompt injection in the context of LLMs?",
                "answers": [
                    {"id": "a", "text": "Injecting malicious code into the model's training data", "correct": False},
                    {"id": "b", "text": "Crafting input that tricks the LLM into ignoring its instructions and safety controls", "correct": True},
                    {"id": "c", "text": "Adding unauthorized plugins to the LLM", "correct": False},
                    {"id": "d", "text": "Overloading the model with too many concurrent requests", "correct": False}
                ]
            },
            {
                "question": "What is the purpose of Microsoft Purview AI hub?",
                "answers": [
                    {"id": "a", "text": "To train AI models using enterprise data", "correct": False},
                    {"id": "b", "text": "To govern AI assets, track usage, and ensure compliance across AI deployments", "correct": True},
                    {"id": "c", "text": "To replace Azure OpenAI Service", "correct": False},
                    {"id": "d", "text": "To generate AI content for marketing", "correct": False}
                ]
            },
            {
                "question": "What does MITRE ATLAS provide for AI security?",
                "answers": [
                    {"id": "a", "text": "Pre-built AI models for deployment", "correct": False},
                    {"id": "b", "text": "A framework mapping real-world AI attacks to tactics and techniques", "correct": True},
                    {"id": "c", "text": "Encryption standards for AI workloads", "correct": False},
                    {"id": "d", "text": "Automated penetration testing for AI systems", "correct": False}
                ]
            }
        ]
    }
]
LESSONS = rewrite_lessons_dialogues(LESSONS)
