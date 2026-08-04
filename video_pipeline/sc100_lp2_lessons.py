from dialogue_rewriter import rewrite_lessons_dialogues


LESSONS = [
    {
        "concept_slug": "identity-access",
        "title": "Microsoft Entra ID: Your Identity Foundation",
        "slug": "sc100-entra-id-fundamentals",
        "description": "Understanding Microsoft Entra ID as the cloud-native identity platform powering modern enterprise security.",
        "hook": "Every breach starts with identity. If your identity layer is weak, nothing else matters.",
        "problem": "Organizations still think on-prem Active Directory is enough in a cloud-first world, leaving gaps attackers love to exploit.",
        "explanation": "Microsoft Entra ID is Azure Active Directory rebranded — a cloud-native identity and access management service. It manages users, groups, service principals, and managed identities across cloud apps. Unlike on-prem AD, it's globally distributed and scales infinitely. Hybrid models use Entra Connect or Cloud Sync to bridge both worlds.",
        "real_world_example": "A company migrating to Microsoft 365 discovers their on-prem AD has 200 stale accounts. Entra ID's sync reveals the gaps, and they disable dormant access before an attacker can use it.",
        "summary": "Entra ID is your identity foundation in the cloud. Understanding its objects, tenants, and hybrid models is step one for every SC-100 domain.",
        "curiosity_hook": "Did you know a single compromised service principal can give an attacker lateral movement across your entire cloud estate without ever touching a user account?",
        "dialogue": [
            {"speaker": "Peter", "text": "So wait, Entra ID is just Azure AD with a new name? Why rebrand at all?"},
            {"speaker": "Stewie", "text": "Because Azure AD does way more than directory services now. Entra is the whole identity fabric."},
            {"speaker": "Peter", "text": "Okay but how is it different from regular Active Directory?"},
            {"speaker": "Stewie", "text": "AD lives on your servers. Entra ID lives in the cloud — globally distributed, no domain controllers needed."},
            {"speaker": "Peter", "text": "What about service principals? That sounds made up."},
            {"speaker": "Stewie", "text": "They're identities for apps and services. Think of them as the app equivalent of a user account."},
            {"speaker": "Peter", "text": "And managed identities?"},
            {"speaker": "Stewie", "text": "Azure handles the credentials for you. No secrets in code, no rotation headaches. Beautiful."},
            {"speaker": "Peter", "text": "What if we're still running on-prem AD though?"},
            {"speaker": "Stewie", "text": "That's hybrid identity. Entra Connect syncs your local directory to the cloud seamlessly."},
            {"speaker": "Peter", "text": "So you can use both at the same time?"},
            {"speaker": "Stewie", "text": "Exactly. Most enterprises run hybrid for years during migration. It's the norm, not the exception."},
        ],
        "learning_objectives": [
            "Explain what Microsoft Entra ID is and how it differs from on-premises Active Directory",
            "Identify the core object types in Entra ID: users, groups, service principals, and managed identities",
            "Describe hybrid identity models and the role of Entra Connect and Cloud Sync",
            "Understand why cloud-native identity is foundational to Zero Trust security"
        ],
        "quiz_questions": [
            {
                "question": "Which Entra ID object represents an application or service that needs to access resources?",
                "answers": [
                    {"id": "a", "text": "Managed identity", "correct": False},
                    {"id": "b", "text": "Service principal", "correct": True},
                    {"id": "c", "text": "Security group", "correct": False},
                    {"id": "d", "text": "Guest user", "correct": False}
                ]
            },
            {
                "question": "What tool syncs on-premises Active Directory objects into Microsoft Entra ID?",
                "answers": [
                    {"id": "a", "text": "Azure Migrate", "correct": False},
                    {"id": "b", "text": "Entra Connect", "correct": True},
                    {"id": "c", "text": "Microsoft Purview", "correct": False},
                    {"id": "d", "text": "Azure Arc", "correct": False}
                ]
            },
            {
                "question": "Which statement about Entra ID is TRUE compared to on-prem AD?",
                "answers": [
                    {"id": "a", "text": "It requires domain controllers in each datacenter", "correct": False},
                    {"id": "b", "text": "It is a cloud-native, globally distributed identity service", "correct": True},
                    {"id": "c", "text": "It only supports Windows-based authentication", "correct": False},
                    {"id": "d", "text": "It cannot sync with on-premises directories", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "identity-access",
        "title": "Authentication Methods & Passwordless",
        "slug": "sc100-authentication-methods",
        "description": "Exploring modern authentication methods from MFA to fully passwordless sign-in with FIDO2 and passkeys.",
        "hook": "Passwords are the weakest link in security. The future is passwordless — and it's already here.",
        "problem": "Password-based attacks account for the vast majority of breaches, yet organizations cling to passwords out of habit.",
        "explanation": "Microsoft Entra ID supports MFA via Authenticator app, SMS, voice calls, and OATH tokens. But the real evolution is passwordless: FIDO2 security keys, Windows Hello for Business, and certificate-based authentication use public-private key pairs — no shared secret to steal. Passkeys are the latest standard, syncing across devices while remaining phishing-resistant.",
        "real_world_example": "A financial firm deploys FIDO2 keys to traders. Even if a trader clicks a phishing link, the attacker can't replay the hardware-bound credential — the attack fails.",
        "summary": "MFA is essential, but passwordless authentication using FIDO2, passkeys, and Windows Hello eliminates entire categories of credential attacks.",
        "curiosity_hook": "Passkeys use the same cryptographic principle as TLS certificates — your private key never leaves your device. Ever wonder why phishers can't steal them?",
        "dialogue": [
            {"speaker": "Peter", "text": "I keep hearing passwordless is the future. Is it actually real?"},
            {"speaker": "Stewie", "text": "It's the present. FIDO2 keys, passkeys, Windows Hello — all production-ready right now."},
            {"speaker": "Peter", "text": "But how does it work without a password?"},
            {"speaker": "Stewie", "text": "Public-private key pairs. Your device holds the private key. The server holds the public key."},
            {"speaker": "Peter", "text": "What about the Authenticator app? That's still a password thing right?"},
            {"speaker": "Stewie", "text": "It's push-based MFA. You approve a login on your phone. Way better than SMS codes."},
            {"speaker": "Peter", "text": "Can someone steal my FIDO2 key?"},
            {"speaker": "Stewie", "text": "Physical theft yes. But remote phishing? Impossible. The key is hardware-bound and origin-locked."},
            {"speaker": "Peter", "text": "So passkeys are just a fancier FIDO2?"},
            {"speaker": "Stewie", "text": "Passkeys sync across your devices for convenience while staying phish-resistant. Best of both worlds."},
            {"speaker": "Peter", "text": "What if someone loses their security key?"},
            {"speaker": "Stewie", "text": "You register a backup key or use the Authenticator app. Always have a second factor registered."},
        ],
        "learning_objectives": [
            "Compare MFA methods including Microsoft Authenticator, SMS, voice, and OATH tokens",
            "Explain how passwordless authentication uses public-private key pairs to eliminate credential theft",
            "Describe FIDO2 security keys, Windows Hello for Business, and passkeys as passwordless solutions",
            "Understand registration campaigns and combined security information registration in Entra ID"
        ],
        "quiz_questions": [
            {
                "question": "Why is FIDO2 authentication resistant to phishing?",
                "answers": [
                    {"id": "a", "text": "It uses SMS codes that expire quickly", "correct": False},
                    {"id": "b", "text": "The private key is hardware-bound and origin-locked", "correct": True},
                    {"id": "c", "text": "It requires a biometric scan on the server", "correct": False},
                    {"id": "d", "text": "It uses rotating passwords generated locally", "correct": False}
                ]
            },
            {
                "question": "What does a passkey add on top of standard FIDO2?",
                "answers": [
                    {"id": "a", "text": "Syncing across devices for convenience", "correct": True},
                    {"id": "b", "text": "Stronger encryption than FIDO2", "correct": False},
                    {"id": "c", "text": "Integration with legacy applications", "correct": False},
                    {"id": "d", "text": "Elimination of all MFA requirements", "correct": False}
                ]
            },
            {
                "question": "What feature helps drive adoption of passwordless methods in an organization?",
                "answers": [
                    {"id": "a", "text": "Azure Policy enforcement", "correct": False},
                    {"id": "b", "text": "Entra ID registration campaigns", "correct": True},
                    {"id": "c", "text": "Conditional Access lockdown", "correct": False},
                    {"id": "d", "text": "PIM role activation", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "identity-access",
        "title": "Conditional Access: Your Security Gateway",
        "slug": "sc100-conditional-access",
        "description": "How Conditional Access policies act as if-then decision engines enforcing access controls in real time.",
        "hook": "Conditional Access is the brain behind Zero Trust — it evaluates every sign-in and decides: allow, block, or challenge.",
        "problem": "Static security perimeters don't work when users access resources from anywhere. You need dynamic, context-aware access control.",
        "explanation": "Conditional Access uses an if-then model: IF signals match (user, location, device, app, risk level), THEN enforce controls (require MFA, block access, limit session). Named locations and trusted IPs help define corporate networks. Policies have priority ordering, and report-only mode lets you test before enforcing. The what-if tool simulates policy impact.",
        "real_world_example": "A company uses Conditional Access to block all sign-ins from outside the country, then adds an exception requiring MFA for traveling executives — stopping credential stuffing attacks that originate overseas.",
        "summary": "Conditional Access evaluates signals in real time and applies access controls, making it the policy engine at the core of Zero Trust identity.",
        "curiosity_hook": "A single Conditional Access policy can prevent more breaches than an entire firewall — because it's evaluating context, not just packets.",
        "dialogue": [
            {"speaker": "Peter", "text": "Conditional Access sounds like a bouncer at a club. Is that basically it?"},
            {"speaker": "Stewie", "text": "That's actually a perfect analogy. It checks your ID, who you're with, and where you came from."},
            {"speaker": "Peter", "text": "So what are the signals it checks?"},
            {"speaker": "Stewie", "text": "User identity, location, device compliance, app being accessed, and real-time risk level."},
            {"speaker": "Peter", "text": "And the controls? Like what it actually does?"},
            {"speaker": "Stewie", "text": "Grant access, require MFA, block entirely, or restrict the session. Classic if-then logic."},
            {"speaker": "Peter", "text": "What are named locations?"},
            {"speaker": "Stewie", "text": "IP ranges you define as trusted. Corporate offices, VPN endpoints. Different treatment for those."},
            {"speaker": "Peter", "text": "Can you test policies before going live?"},
            {"speaker": "Stewie", "text": "Report-only mode shows what would happen without enforcing. Plus the what-if tool."},
            {"speaker": "Peter", "text": "What if two policies conflict?"},
            {"speaker": "Stewie", "text": "Most restrictive wins. Priority ordering controls which evaluates first."},
        ],
        "learning_objectives": [
            "Explain the if-then structure of Conditional Access policies and their core signals",
            "Differentiate between grant controls, session controls, and access block actions",
            "Describe the role of named locations, trusted IPs, and policy priority in policy evaluation",
            "Use report-only mode and the what-if tool to safely test Conditional Access policies"
        ],
        "quiz_questions": [
            {
                "question": "What happens when two Conditional Access policies with conflicting controls apply to the same sign-in?",
                "answers": [
                    {"id": "a", "text": "The most recently created policy wins", "correct": False},
                    {"id": "b", "text": "The most restrictive policy is enforced", "correct": True},
                    {"id": "c", "text": "Both policies are ignored", "correct": False},
                    {"id": "d", "text": "The user chooses which to follow", "correct": False}
                ]
            },
            {
                "question": "Which tool lets you simulate how Conditional Access policies would affect a sign-in without enforcing them?",
                "answers": [
                    {"id": "a", "text": "Report-only mode", "correct": False},
                    {"id": "b", "text": "What-if tool", "correct": True},
                    {"id": "c", "text": "Sign-in logs", "correct": False},
                    {"id": "d", "text": "Audit mode", "correct": False}
                ]
            },
            {
                "question": "What is the primary purpose of named locations in Conditional Access?",
                "answers": [
                    {"id": "a", "text": "To track user geolocation history", "correct": False},
                    {"id": "b", "text": "To define trusted IP ranges for policy evaluation", "correct": True},
                    {"id": "c", "text": "To map physical office locations in Azure", "correct": False},
                    {"id": "d", "text": "To restrict Azure resource deployments by region", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "identity-access",
        "title": "Microsoft Entra ID Protection",
        "slug": "sc100-entra-id-protection",
        "description": "Leveraging AI-driven risk detection and automated remediation to protect identities in real time.",
        "hook": "Entra ID Protection uses Microsoft's massive threat intelligence to detect risks humans would miss — in real time.",
        "problem": "Manual monitoring of sign-ins and user behavior is impossible at scale. Attackers hide in the noise of millions of events.",
        "explanation": "Entra ID Protection detects sign-in risks (impossible travel, unfamiliar locations, leaked credentials) and user risks (anomalous activity, compromised accounts). Risk levels are low, medium, or high. Automated policies can trigger MFA, block access, or force password resets. The MFA registration policy ensures all users have MFA configured before risk events occur.",
        "real_world_example": "An employee's credentials appear on a dark web paste site. Entra ID Protection flags the user risk automatically, forces a password reset, and blocks the account — all before the attacker tries the credentials.",
        "summary": "Entra ID Protection uses machine learning to detect identity risks and automate remediation, catching threats that rule-based systems miss.",
        "curiosity_hook": "Microsoft processes over 65 trillion signals daily. Entra ID Protection taps into that intelligence to score your sign-ins in real time.",
        "dialogue": [
            {"speaker": "Peter", "text": "How does Entra ID Protection actually detect risks? Is it just checking IP addresses?"},
            {"speaker": "Stewie", "text": "Way deeper. It uses threat intelligence across trillions of signals — location, behavior, leaked credentials."},
            {"speaker": "Peter", "text": "What's impossible travel? That sounds like a sci-fi concept."},
            {"speaker": "Stewie", "text": "Someone signs in from New York and five minutes later from Tokyo. Impossible unless credentials are stolen."},
            {"speaker": "Peter", "text": "And user risk vs sign-in risk — what's the difference?"},
            {"speaker": "Stewie", "text": "Sign-in risk is about that specific login event. User risk is about the account being compromised."},
            {"speaker": "Peter", "text": "So what happens when a risk is detected?"},
            {"speaker": "Stewie", "text": "Automated policies kick in. Require MFA, block access, or force a password reset."},
            {"speaker": "Peter", "text": "Can you set up the MFA registration before any risk happens?"},
            {"speaker": "Stewie", "text": "Yes! The MFA registration policy enrolls users proactively so they're protected when risk hits."},
            {"speaker": "Peter", "text": "So it's like putting on a seatbelt before you drive, not after the crash."},
            {"speaker": "Stewie", "text": "That's... actually a great analogy. I'm almost impressed."},
        ],
        "learning_objectives": [
            "Differentiate between sign-in risks and user risks and their respective detection methods",
            "Identify key risk detection types: impossible travel, unfamiliar locations, and leaked credentials",
            "Explain automated remediation policies including MFA requirements, blocking, and password resets",
            "Describe the role of the MFA registration policy in proactive identity protection"
        ],
        "quiz_questions": [
            {
                "question": "What type of risk does Entra ID Protection detect when a user account's credentials appear on a dark web paste site?",
                "answers": [
                    {"id": "a", "text": "Sign-in risk only", "correct": False},
                    {"id": "b", "text": "User risk", "correct": True},
                    {"id": "c", "text": "Device risk", "correct": False},
                    {"id": "d", "text": "Application risk", "correct": False}
                ]
            },
            {
                "question": "Which automated action can an Entra ID Protection sign-in risk policy trigger for high-risk sign-ins?",
                "answers": [
                    {"id": "a", "text": "Force device compliance check", "correct": False},
                    {"id": "b", "text": "Block access or require MFA", "correct": True},
                    {"id": "c", "text": "Revoke all refresh tokens only", "correct": False},
                    {"id": "d", "text": "Send alert email to the user", "correct": False}
                ]
            },
            {
                "question": "What is the purpose of the MFA registration policy in Entra ID Protection?",
                "answers": [
                    {"id": "a", "text": "To enforce MFA only after a risk is detected", "correct": False},
                    {"id": "b", "text": "To proactively ensure all users register for MFA before risk events occur", "correct": True},
                    {"id": "c", "text": "To disable MFA for low-risk users", "correct": False},
                    {"id": "d", "text": "To manage FIDO2 key distribution", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "privileged-access",
        "title": "Privileged Access Management with PIM",
        "slug": "sc100-pim-privileged-access",
        "description": "Controlling, monitoring, and governing privileged access using Microsoft Entra Privileged Identity Management.",
        "hook": "Admin accounts are the crown jewels. PIM ensures nobody wears the crown unless they absolutely need to — and only for a moment.",
        "problem": "Standing admin permissions are a disaster waiting to happen. Most breaches exploit privileges that were never needed in the first place.",
        "explanation": "PIM follows the Enterprise Access Model with tiering: T0 (global admin-level), T1 (domain/subscription), T2 (application). PIM for Entra ID roles offers eligible vs active assignments with time limits and approval workflows. PIM for Azure Resources extends JIT activation to resource roles. PIM for Groups lets you govern membership of privileged groups. Access reviews keep assignments current.",
        "real_world_example": "An admin needs Global Administrator for 30 minutes to fix a tenant configuration. PIM grants eligible access, they activate with approval, complete the task, and the role automatically expires — limiting blast radius.",
        "summary": "PIM enforces least privilege through time-bound, approval-required, and monitored role assignments across Entra ID and Azure resources.",
        "curiosity_hook": "The average organization has 10x more privileged users than they think. PIM's access reviews often reveal dormant admin accounts nobody knew existed.",
        "dialogue": [
            {"speaker": "Peter", "text": "Why can't admins just have permanent access? It's faster right?"},
            {"speaker": "Stewie", "text": "Faster until their account gets compromised and the attacker has global admin forever."},
            {"speaker": "Peter", "text": "So PIM fixes that how exactly?"},
            {"speaker": "Stewie", "text": "Eligible assignments mean you request the role when needed. It activates for a limited time then expires."},
            {"speaker": "Peter", "text": "What's the difference between PIM for Entra roles and Azure resources?"},
            {"speaker": "Stewie", "text": "Entra roles control identity management. Azure resource roles control access to subscriptions and resources."},
            {"speaker": "Peter", "text": "And PIM for Groups?"},
            {"speaker": "Stewie", "text": "It governs membership of privileged groups. Time-bound membership with approval workflows."},
            {"speaker": "Peter", "text": "What about approvals? Who approves the activation?"},
            {"speaker": "Stewie", "text": "You can require multi-level approvals, business justification, or access packages for governance."},
            {"speaker": "Peter", "text": "How does this tie into the Enterprise Access Model?"},
            {"speaker": "Stewie", "text": "EAM defines tiering — T0 is most sensitive. PIM enforces controls at each tier."},
        ],
        "learning_objectives": [
            "Explain the Enterprise Access Model and tiering approach for privileged access",
            "Differentiate between eligible and active role assignments in PIM for Entra ID",
            "Describe JIT activation, approval workflows, and time-limited access in PIM",
            "Understand PIM for Azure Resources, PIM for Groups, and access review integration"
        ],
        "quiz_questions": [
            {
                "question": "In PIM, what is an eligible role assignment?",
                "answers": [
                    {"id": "a", "text": "A permanent admin role with full permissions", "correct": False},
                    {"id": "b", "text": "A role that can be activated on-demand with time limits and conditions", "correct": True},
                    {"id": "c", "text": "A read-only role for monitoring purposes", "correct": False},
                    {"id": "d", "text": "A role assigned to all users by default", "correct": False}
                ]
            },
            {
                "question": "Which tier in the Enterprise Access Model represents the most sensitive privileged access?",
                "answers": [
                    {"id": "a", "text": "T2 - Application", "correct": False},
                    {"id": "b", "text": "T1 - Domain and subscription", "correct": False},
                    {"id": "c", "text": "T0 - Global admin level", "correct": True},
                    {"id": "d", "text": "All tiers are equal sensitivity", "correct": False}
                ]
            },
            {
                "question": "What happens to stale privileged role assignments managed by PIM?",
                "answers": [
                    {"id": "a", "text": "They remain active indefinitely", "correct": False},
                    {"id": "b", "text": "Access reviews periodically evaluate and revoke them if unjustified", "correct": True},
                    {"id": "c", "text": "They are automatically upgraded to higher tiers", "correct": False},
                    {"id": "d", "text": "They are archived but never removed", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "privileged-access",
        "title": "Just-in-Time & Just-Enough Access",
        "slug": "sc100-jit-jea-access",
        "description": "Eliminating standing privileges with JIT activation and JEA scoping to minimize attack surface.",
        "hook": "Standing permissions are like leaving the vault open 'just in case.' JIT and JEA close the vault and only open it when needed.",
        "problem": "Over-provisioned accounts are the number one target in breaches. Attackers don't need to escalate privileges if you've already given them everything.",
        "explanation": "Just-in-Time (JIT) access means privileges are granted only when needed and expire automatically. Just-Enough Access (JEA) limits what you can do even when elevated — using role capabilities and session configurations. Privileged Access Workstations (PAWs) and Secure Administrative Hosts (SAH) provide hardened environments for admin tasks. Together, these form the backbone of Zero Trust privileged access.",
        "real_world_example": "A helpdesk technician uses JIT to request Domain Admin for 15 minutes to reset a critical service account. JEA restricts them to only the Reset-Password command. The session is logged and the role auto-expires.",
        "summary": "JIT removes standing privileges, JEA scopes what elevated users can do, and PAWs harden the admin experience — all essential Zero Trust patterns.",
        "curiosity_hook": "Microsoft found that 95% of Azure AD compromises don't use admin accounts at all — they compromise regular accounts and move laterally. JEA stops lateral movement cold.",
        "dialogue": [
            {"speaker": "Peter", "text": "Why is standing permission such a big problem?"},
            {"speaker": "Stewie", "text": "If an attacker compromises an account with permanent admin rights, they own everything. No barriers."},
            {"speaker": "Peter", "text": "So JIT just turns on permissions when you need them?"},
            {"speaker": "Stewie", "text": "Exactly. You activate, do your work, and the access automatically expires. Time-boxed elevation."},
            {"speaker": "Peter", "text": "And JEA is different from JIT?"},
            {"speaker": "Stewie", "text": "JIT controls WHEN you get access. JEA controls WHAT you can do with it. Even elevated users get limited."},
            {"speaker": "Peter", "text": "So even with admin access I can't run everything?"},
            {"speaker": "Stewie", "text": "Right. Role capabilities define exactly which cmdlets are allowed. No surprise commands."},
            {"speaker": "Peter", "text": "What's a PAW? Sounds like a dog toy."},
            {"speaker": "Stewie", "text": "Privileged Access Workstation. A hardened, dedicated machine for admin tasks. No email, no browsing."},
            {"speaker": "Peter", "text": "Do I really need a separate computer just for admin work?"},
            {"speaker": "Stewie", "text": "For high-security environments, absolutely. It's the cleanest way to protect sensitive operations."},
        ],
        "learning_objectives": [
            "Explain why standing permissions create unnecessary risk and how JIT access mitigates it",
            "Describe Just-Enough Access and how role capabilities and session configurations limit elevation",
            "Identify the role of Privileged Access Workstations and Secure Administrative Hosts",
            "Connect JIT, JEA, and PAW concepts to the broader Zero Trust security framework"
        ],
        "quiz_questions": [
            {
                "question": "How does Just-in-Time (JIT) access differ from traditional standing permissions?",
                "answers": [
                    {"id": "a", "text": "JIT grants permanent access with logging", "correct": False},
                    {"id": "b", "text": "JIT grants time-limited access that expires automatically", "correct": True},
                    {"id": "c", "text": "JIT requires no approval process", "correct": False},
                    {"id": "d", "text": "JIT only applies to Azure resources, not Entra ID", "correct": False}
                ]
            },
            {
                "question": "What does Just-Enough Access (JEA) control?",
                "answers": [
                    {"id": "a", "text": "The time window for admin access", "correct": False},
                    {"id": "b", "text": "The specific commands and functions an elevated user can execute", "correct": True},
                    {"id": "c", "text": "The physical location of the admin workstation", "correct": False},
                    {"id": "d", "text": "The number of concurrent admin sessions", "correct": False}
                ]
            },
            {
                "question": "What is a Privileged Access Workstation (PAW)?",
                "answers": [
                    {"id": "a", "text": "A regular laptop with antivirus installed", "correct": False},
                    {"id": "b", "text": "A hardened, dedicated device for performing sensitive administrative tasks", "correct": True},
                    {"id": "c", "text": "A cloud-based admin portal in Azure", "correct": False},
                    {"id": "d", "text": "A backup server for admin credentials", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "identity-access",
        "title": "Identity Governance & Lifecycle",
        "slug": "sc100-identity-governance",
        "description": "Managing who has access to what, for how long, and why — through entitlement management and lifecycle automation.",
        "hook": "Access governance ensures the right people have the right access at the right time — and loses it when they no longer need it.",
        "problem": "Manual access provisioning and deprovisioning leads to over-privileged users, orphaned accounts, and compliance nightmares.",
        "explanation": "Entitlement Management uses access packages bundled in catalogs with policies for assignment and approval. Access Reviews periodically certify that access is still needed, triggered by events or schedules. Lifecycle Workflows automate onboarding, offboarding, and attribute-based transitions — like removing access when someone changes departments. These tools close the identity lifecycle gap.",
        "real_world_example": "An employee transfers from Finance to Engineering. Lifecycle Workflow detects the department attribute change, removes Finance access packages, and triggers an access review for shared resources — all automatic.",
        "summary": "Identity governance automates access lifecycle from request to removal, ensuring compliance and eliminating orphaned permissions.",
        "curiosity_hook": "The average enterprise employee accumulates access to 40+ applications within their first year. Without governance, most of that access never gets reviewed.",
        "dialogue": [
            {"speaker": "Peter", "text": "What exactly is entitlement management? Big words intimidate me."},
            {"speaker": "Stewie", "text": "It's just organized access. Bundle permissions into access packages, put them in catalogs, control who gets them."},
            {"speaker": "Peter", "text": "So it's like a shopping catalog for permissions?"},
            {"speaker": "Stewie", "text": "Sort of! Users request an access package, it goes through approval, and they get exactly what they need."},
            {"speaker": "Peter", "text": "And access reviews are like an audit?"},
            {"speaker": "Stewie", "text": "Periodic reviews where managers confirm people still need access. If not, it's revoked."},
            {"speaker": "Peter", "text": "What about when someone leaves the company?"},
            {"speaker": "Stewie", "text": "Lifecycle Workflows handle that automatically. Offboarding removes access, revokes sessions, cleans up."},
            {"speaker": "Peter", "text": "Can it handle internal moves too? Like department transfers?"},
            {"speaker": "Stewie", "text": "Yes! Attribute-based workflows trigger when department or role changes. Access adjusts automatically."},
            {"speaker": "Peter", "text": "How do you justify all this to management?"},
            {"speaker": "Stewie", "text": "Business justification is part of the access request. Users explain why, creating an auditable trail."},
        ],
        "learning_objectives": [
            "Explain entitlement management using access packages, catalogs, and assignment policies",
            "Describe the purpose and triggers for access reviews and certification campaigns",
            "Understand lifecycle workflows for onboarding, offboarding, and attribute-based transitions",
            "Connect identity governance to compliance requirements and business justification"
        ],
        "quiz_questions": [
            {
                "question": "What is an access package in entitlement management?",
                "answers": [
                    {"id": "a", "text": "A single Azure resource with role assignments", "correct": False},
                    {"id": "b", "text": "A bundle of access rights with policies governing who can request and approve them", "correct": True},
                    {"id": "c", "text": "A license type for Microsoft 365", "correct": False},
                    {"id": "d", "text": "A compliance template for audits", "correct": False}
                ]
            },
            {
                "question": "What triggers a lifecycle workflow for an employee transferring departments?",
                "answers": [
                    {"id": "a", "text": "Manual request from IT helpdesk", "correct": False},
                    {"id": "b", "text": "Attribute change in the user's profile, such as department update", "correct": True},
                    {"id": "c", "text": "Expiration of their access package", "correct": False},
                    {"id": "d", "text": "A failed login attempt", "correct": False}
                ]
            },
            {
                "question": "Why is business justification important in entitlement management?",
                "answers": [
                    {"id": "a", "text": "It replaces the need for manager approval", "correct": False},
                    {"id": "b", "text": "It creates an auditable record of why access was requested", "correct": True},
                    {"id": "c", "text": "It automatically grants access to all packages", "correct": False},
                    {"id": "d", "text": "It disables access after a set period", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "identity-access",
        "title": "External Identity: B2B & B2C",
        "slug": "sc100-external-identity",
        "description": "Managing identities for partners, guests, and customers through B2B collaboration and External ID solutions.",
        "hook": "Your security perimeter now includes every partner, vendor, and customer who touches your data. External identity makes that manageable.",
        "problem": "Organizations share data with hundreds of external partners but manage guest access with spreadsheets and ad hoc processes.",
        "explanation": "B2B collaboration lets you invite external users as guest accounts in your Entra ID tenant, with cross-tenant access settings governing trust. Direct Connect enables mutual identity sharing with specific organizations. Azure AD B2C provides customer identity with custom policies and user flows. External ID unifies these under one platform. Cross-tenant synchronization automates user provisioning across tenants.",
        "real_world_example": "A consulting firm uses B2B Direct Connect with three major clients. Each client's employees authenticate with their own Entra ID — no separate accounts to manage, no passwords to share, full audit trail.",
        "summary": "External identity solutions let you collaborate securely with partners and serve customers while maintaining control over authentication and authorization.",
        "curiosity_hook": "Microsoft estimates that over 50% of Entra ID tenants have at least one guest user. Most organizations are already doing B2B — they just don't have governance around it.",
        "dialogue": [
            {"speaker": "Peter", "text": "What's the difference between B2B and B2C? The names confuse me."},
            {"speaker": "Stewie", "text": "B2B is for partners and collaborators. B2C is for your end customers. Different audiences, different needs."},
            {"speaker": "Peter", "text": "So B2B just creates guest accounts in my tenant?"},
            {"speaker": "Stewie", "text": "Exactly. Guests authenticate with their own credentials. You control what they access in your environment."},
            {"speaker": "Peter", "text": "What about Direct Connect? How's that different from regular B2B?"},
            {"speaker": "Stewie", "text": "Direct Connect is bidirectional. Both orgs trust each other's users without creating guest accounts."},
            {"speaker": "Peter", "text": "And B2C is for customers who aren't in any enterprise directory?"},
            {"speaker": "Stewie", "text": "Right. B2C provides social logins, custom sign-up flows, and identity management for your customers."},
            {"speaker": "Peter", "text": "Can I use Conditional Access on B2B guests?"},
            {"speaker": "Stewie", "text": "Absolutely. Cross-tenant access settings and CA policies apply to guests just like internal users."},
            {"speaker": "Peter", "text": "What's cross-tenant synchronization then?"},
            {"speaker": "Stewie", "text": "It automatically provisions users from one tenant to another. No manual invites for ongoing collaboration."},
        ],
        "learning_objectives": [
            "Differentiate between B2B collaboration, Direct Connect, and Azure AD B2C use cases",
            "Explain how guest users authenticate and how cross-tenant access settings govern trust",
            "Describe cross-tenant synchronization and its benefits for ongoing collaboration",
            "Understand how Conditional Access policies extend to external identities"
        ],
        "quiz_questions": [
            {
                "question": "How do B2B guest users authenticate in your Entra ID tenant?",
                "answers": [
                    {"id": "a", "text": "They create a new account in your tenant with a local password", "correct": False},
                    {"id": "b", "text": "They authenticate with their own home tenant credentials", "correct": True},
                    {"id": "c", "text": "They use a shared service account for all guests", "correct": False},
                    {"id": "d", "text": "They cannot authenticate and are read-only", "correct": False}
                ]
            },
            {
                "question": "What does Azure AD B2C primarily provide?",
                "answers": [
                    {"id": "a", "text": "Partner collaboration with enterprise tenants", "correct": False},
                    {"id": "b", "text": "Customer identity management with social logins and custom sign-up flows", "correct": True},
                    {"id": "c", "text": "Internal employee lifecycle management", "correct": False},
                    {"id": "d", "text": "Cross-tenant administrative access", "correct": False}
                ]
            },
            {
                "question": "What is the key benefit of B2B Direct Connect over standard B2B collaboration?",
                "answers": [
                    {"id": "a", "text": "It requires no authentication", "correct": False},
                    {"id": "b", "text": "It provides bidirectional trust without manual guest account creation", "correct": True},
                    {"id": "c", "text": "It works only with personal Microsoft accounts", "correct": False},
                    {"id": "d", "text": "It eliminates the need for Conditional Access", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "compliance",
        "title": "Microsoft Purview Compliance Manager",
        "slug": "sc100-compliance-manager",
        "description": "Measuring, managing, and improving your compliance posture with Compliance Score and assessment templates.",
        "hook": "Compliance isn't a checkbox — it's a continuous journey. Compliance Manager gives you a score and a roadmap.",
        "problem": "Organizations struggle to measure compliance across multiple regulatory frameworks, leading to audit fatigue and gaps.",
        "explanation": "Compliance Manager calculates a Compliance Score based on your completion of improvement actions across controls. Assessment templates map to standards like GDPR, HIPAA, PCI DSS, and ISO 27001. In the shared responsibility model, cloud providers secure the infrastructure while you secure your data. Compliance Manager tracks both technical and operational controls, distinguishing between audit findings and actionable improvement steps.",
        "real_world_example": "A healthcare startup uses the HIPAA template in Compliance Manager. Their score starts at 32%. Within six months of completing priority actions, they reach 78% — documented and ready for their first audit.",
        "summary": "Compliance Manager quantifies your compliance posture, maps improvement actions to regulatory templates, and tracks progress continuously.",
        "curiosity_hook": "Compliance Score weights improvement actions by impact — fixing one critical control can move your score more than completing ten minor ones.",
        "dialogue": [
            {"speaker": "Peter", "text": "What is Compliance Score actually measuring?"},
            {"speaker": "Stewie", "text": "It's a percentage based on how many improvement actions you've completed across your compliance controls."},
            {"speaker": "Peter", "text": "So it's just a to-do list with a score attached?"},
            {"speaker": "Stewie", "text": "A sophisticated to-do list. It maps controls to regulatory frameworks and prioritizes by risk impact."},
            {"speaker": "Peter", "text": "What templates are available?"},
            {"speaker": "Stewie", "text": "GDPR, HIPAA, PCI DSS, ISO 27001, NIST, and many more. Each maps controls to that regulation."},
            {"speaker": "Peter", "text": "What's the shared responsibility model?"},
            {"speaker": "Stewie", "text": "Microsoft secures the cloud platform. You secure your data, configs, and access within it."},
            {"speaker": "Peter", "text": "Does it distinguish between audit and assessment?"},
            {"speaker": "Stewie", "text": "Yes. Audits verify controls are in place. Assessments identify gaps and recommend improvements."},
            {"speaker": "Peter", "text": "Can I use it for continuous monitoring?"},
            {"speaker": "Stewie", "text": "That's the whole point. It continuously evaluates your posture and highlights what needs attention."},
        ],
        "learning_objectives": [
            "Explain how Compliance Score is calculated and what improvement actions represent",
            "Identify major assessment templates including GDPR, HIPAA, PCI DSS, and ISO 27001",
            "Describe the shared responsibility model and how it affects compliance obligations",
            "Understand the difference between audits, assessments, and continuous compliance monitoring"
        ],
        "quiz_questions": [
            {
                "question": "What determines the weighting of improvement actions in Compliance Score?",
                "answers": [
                    {"id": "a", "text": "The number of users affected", "correct": False},
                    {"id": "b", "text": "The risk impact of the control on your compliance posture", "correct": True},
                    {"id": "c", "text": "The cost of implementing the action", "correct": False},
                    {"id": "d", "text": "The age of the control definition", "correct": False}
                ]
            },
            {
                "question": "In the shared responsibility model, what is the customer's primary obligation?",
                "answers": [
                    {"id": "a", "text": "Securing the physical datacenter", "correct": False},
                    {"id": "b", "text": "Securing their data, configurations, and access within the cloud platform", "correct": True},
                    {"id": "c", "text": "Managing network hardware in the cloud", "correct": False},
                    {"id": "d", "text": "Patching the hypervisor layer", "correct": False}
                ]
            },
            {
                "question": "Which regulation does a PCI DSS assessment template primarily address?",
                "answers": [
                    {"id": "a", "text": "Healthcare data privacy", "correct": False},
                    {"id": "b", "text": "Payment card data security", "correct": True},
                    {"id": "c", "text": "European personal data protection", "correct": False},
                    {"id": "d", "text": "Government classified information", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "compliance",
        "title": "Azure Policy & Blueprints",
        "slug": "sc100-azure-policy-blueprints",
        "description": "Enforcing organizational standards at scale using Azure Policy definitions, effects, and Blueprint artifact orchestration.",
        "hook": "Azure Policy doesn't ask for permission — it enforces your rules before resources even deploy.",
        "problem": "Without guardrails, teams deploy resources that violate security standards, creating compliance debt that's expensive to fix later.",
        "explanation": "Azure Policy uses definitions and initiatives to enforce rules with effects like deny, audit, append, modify, and deployIfNotExists. Compliance evaluation runs continuously, and remediation tasks fix existing non-compliant resources. Azure Blueprints orchestrate policy assignments, role assignments, ARM templates, and resource groups into repeatable landing zone deployments. Policy Insights provides central visibility into compliance state.",
        "real_world_example": "A company deploys a Blueprint for new subscriptions that automatically applies tagging policies, deploys network security groups, and assigns required RBAC roles — ensuring every new subscription starts compliant.",
        "summary": "Azure Policy and Blueprints provide guardrails and templates that enforce compliance from deployment through the entire resource lifecycle.",
        "curiosity_hook": "The deployIfNotExists effect can automatically provision missing security resources during deployment — you can fix compliance issues before they exist.",
        "dialogue": [
            {"speaker": "Peter", "text": "What's the difference between Azure Policy and Blueprints?"},
            {"speaker": "Stewie", "text": "Policy enforces individual rules. Blueprints bundle multiple policies and resources into a repeatable template."},
            {"speaker": "Peter", "text": "So Blueprints are like a starter kit for new subscriptions?"},
            {"speaker": "Stewie", "text": "Exactly. One Blueprint deploys policies, roles, ARM templates, and resource groups all at once."},
            {"speaker": "Peter", "text": "What effects does Azure Policy support?"},
            {"speaker": "Stewie", "text": "Deny blocks non-compliant deployments. Audit logs violations. Modify adds or removes properties."},
            {"speaker": "Peter", "text": "What about deployIfNotExists?"},
            {"speaker": "Stewie", "text": "It checks if a related resource exists and creates it automatically if missing. Very powerful."},
            {"speaker": "Peter", "text": "Can it fix resources that are already deployed?"},
            {"speaker": "Stewie", "text": "Yes, remediation tasks. They scan existing resources and apply modifications to bring them into compliance."},
            {"speaker": "Peter", "text": "Where do I see all my compliance results?"},
            {"speaker": "Stewie", "text": "Policy Insights in the Azure portal. Central dashboard showing compliant and non-compliant resources."},
        ],
        "learning_objectives": [
            "Explain Azure Policy concepts including definitions, initiatives, and compliance evaluation",
            "Compare policy effects: deny, audit, modify, append, and deployIfNotExists",
            "Describe how Azure Blueprints orchestrate policies, roles, ARM templates, and resource groups",
            "Use Policy Insights and remediation tasks to manage compliance at scale"
        ],
        "quiz_questions": [
            {
                "question": "Which Azure Policy effect automatically provisions a missing related resource during deployment?",
                "answers": [
                    {"id": "a", "text": "Deny", "correct": False},
                    {"id": "b", "text": "Modify", "correct": False},
                    {"id": "c", "text": "deployIfNotExists", "correct": True},
                    {"id": "d", "text": "Append", "correct": False}
                ]
            },
            {
                "question": "What does an Azure Blueprint orchestrate?",
                "answers": [
                    {"id": "a", "text": "Only Azure Policy assignments", "correct": False},
                    {"id": "b", "text": "Policies, role assignments, ARM templates, and resource groups as a repeatable package", "correct": True},
                    {"id": "c", "text": "Only ARM templates for infrastructure deployment", "correct": False},
                    {"id": "d", "text": "Only RBAC role assignments across subscriptions", "correct": False}
                ]
            },
            {
                "question": "What is the purpose of remediation tasks in Azure Policy?",
                "answers": [
                    {"id": "a", "text": "To prevent non-compliant resources from being deployed", "correct": False},
                    {"id": "b", "text": "To fix existing non-compliant resources by applying modifications", "correct": True},
                    {"id": "c", "text": "To delete all non-compliant resources automatically", "correct": False},
                    {"id": "d", "text": "To generate compliance reports for auditors", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "compliance",
        "title": "Insider Risk Management",
        "slug": "sc100-insider-risk-management",
        "description": "Detecting and remediating insider threats using behavioral analytics, machine learning, and adaptive protection.",
        "hook": "The most dangerous threat is the one already inside your walls. Insider Risk Management catches them before they cause damage.",
        "problem": "Traditional security focuses on external attackers, but insiders with legitimate access can cause catastrophic data breaches.",
        "explanation": "Insider Risk Management detects security violations, data theft, data leakage, and data destruction using a risk score algorithm. Activity Explorer provides visibility into user actions. Policy templates target specific insider risk scenarios. Adaptive Protection uses machine learning to tailor DLP policies based on risk levels. Privacy is built in with anonymization and pseudonymization of user data during investigation.",
        "real_world_example": "An employee about to leave the company starts bulk-downloading client data. Insider Risk Management detects the anomaly, raises their risk score, and triggers a DLP policy that blocks USB transfers — all before the data leaves the building.",
        "summary": "Insider Risk Management combines behavioral analytics, ML models, and privacy-by-design principles to detect and prevent insider threats.",
        "curiosity_hook": "Adaptive Protection dynamically adjusts DLP policies based on individual risk scores — a high-risk user gets stricter controls without blanket restrictions for everyone.",
        "dialogue": [
            {"speaker": "Peter", "text": "How do you even detect an insider threat? They have legitimate access."},
            {"speaker": "Stewie", "text": "By analyzing behavior patterns. The risk score algorithm compares actions against baselines and detects anomalies."},
            {"speaker": "Peter", "text": "What kind of behaviors trigger alerts?"},
            {"speaker": "Stewie", "text": "Data theft, unauthorized sharing, bulk downloads, accessing unusual files, destructive actions on data."},
            {"speaker": "Peter", "text": "What's Activity Explorer?"},
            {"speaker": "Stewie", "text": "A dashboard that visualizes user activities across your environment. Helps investigators spot suspicious patterns."},
            {"speaker": "Peter", "text": "But what about employee privacy? Monitoring people feels creepy."},
            {"speaker": "Stewie", "text": "Privacy by design. User data is anonymized during investigation. Only authorized investigators see identities."},
            {"speaker": "Peter", "text": "What's adaptive protection? That sounds like sci-fi."},
            {"speaker": "Stewie", "text": "It uses ML to tailor DLP policies to individual risk levels. High-risk users get stricter controls automatically."},
            {"speaker": "Peter", "text": "So it's not one-size-fits-all?"},
            {"speaker": "Stewie", "text": "Right. A finance exec accessing financial data is normal. Same behavior from marketing? That raises flags."},
        ],
        "learning_objectives": [
            "Identify insider risk indicators: data theft, leakage, destruction, and security violations",
            "Explain how the risk score algorithm and Activity Explorer support insider threat detection",
            "Describe Adaptive Protection and how ML tailors DLP policies to individual risk levels",
            "Understand privacy-by-design principles including anonymization in insider risk investigations"
        ],
        "quiz_questions": [
            {
                "question": "What is the primary purpose of Adaptive Protection in Insider Risk Management?",
                "answers": [
                    {"id": "a", "text": "To apply the same DLP policy to all users uniformly", "correct": False},
                    {"id": "b", "text": "To dynamically tailor DLP policies based on individual user risk scores", "correct": True},
                    {"id": "c", "text": "To monitor all network traffic for external intrusions", "correct": False},
                    {"id": "d", "text": "To enforce password policies across the organization", "correct": False}
                ]
            },
            {
                "question": "How does Insider Risk Management protect employee privacy during investigations?",
                "answers": [
                    {"id": "a", "text": "It disables all monitoring during off-hours", "correct": False},
                    {"id": "b", "text": "It anonymizes user data and limits identity visibility to authorized investigators", "correct": True},
                    {"id": "c", "text": "It only monitors public-facing applications", "correct": False},
                    {"id": "d", "text": "It requires employee consent before any monitoring", "correct": False}
                ]
            },
            {
                "question": "Which insider risk scenario involves an employee bulk-downloading files before resignation?",
                "answers": [
                    {"id": "a", "text": "Security violation", "correct": False},
                    {"id": "b", "text": "Data destruction", "correct": False},
                    {"id": "c", "text": "Data theft", "correct": True},
                    {"id": "d", "text": "Data leakage", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "compliance",
        "title": "Communication Compliance & eDiscovery",
        "slug": "sc100-comm-compliance-ediscovery",
        "description": "Monitoring communications for policy violations and conducting legal investigations with eDiscovery tools.",
        "hook": "Every message, email, and chat is a potential compliance record — and a potential liability if unmonitored.",
        "problem": "Regulatory requirements demand communication monitoring, but manual review of millions of messages is impossible.",
        "explanation": "Communication Compliance monitors Teams, email, and Yammer using built-in and custom ML models, trainable classifiers, and policy conditions. Review workflows route flagged content to investigators. eDiscovery Standard handles basic legal holds and data export. eDiscovery Premium adds custodian management, review sets, OCR, near-duplicate detection, and email threading for complex investigations.",
        "real_world_example": "A bank's Communication Compliance policy flags an employee using insider terminology in Teams chats. The ML model identifies the pattern, routes it for review, and the compliance team investigates before it becomes a regulatory violation.",
        "summary": "Communication Compliance and eDiscovery automate monitoring and investigation of digital communications for regulatory and legal requirements.",
        "curiosity_hook": "eDiscovery Premium's email threading reconstructs conversation chains, saving investigators from reviewing thousands of individual messages to understand context.",
        "dialogue": [
            {"speaker": "Peter", "text": "How does Communication Compliance actually monitor messages? Does it read everything?"},
            {"speaker": "Stewie", "text": "It applies ML models and classifiers to detect policy violations like harassment, data leaks, or regulatory breaches."},
            {"speaker": "Peter", "text": "Can I customize what it looks for?"},
            {"speaker": "Stewie", "text": "Custom policies with specific conditions — keywords, sentiment, ML models, or trainable classifiers you build."},
            {"speaker": "Peter", "text": "What happens when something is flagged?"},
            {"speaker": "Stewie", "text": "It goes into a review workflow. Investigators see flagged content with context and can take action."},
            {"speaker": "Peter", "text": "What's the difference between eDiscovery Standard and Premium?"},
            {"speaker": "Stewie", "text": "Standard handles basic holds and export. Premium adds OCR, deduplication, and email threading."},
            {"speaker": "Peter", "text": "What are custodians in eDiscovery?"},
            {"speaker": "Stewie", "text": "People whose data is relevant to a case. You place legal holds on their mailboxes to preserve evidence."},
            {"speaker": "Peter", "text": "How does this tie into compliance regulations?"},
            {"speaker": "Stewie", "text": "Regulations like GDPR require you to monitor and produce communications on demand. These tools make that possible."},
        ],
        "learning_objectives": [
            "Explain Communication Compliance monitoring for Teams, email, and Yammer with ML models",
            "Describe review workflows and how flagged content is investigated by compliance teams",
            "Differentiate between eDiscovery Standard and eDiscovery Premium capabilities",
            "Understand custodian management, legal holds, and review sets in eDiscovery investigations"
        ],
        "quiz_questions": [
            {
                "question": "What additional capabilities does eDiscovery Premium provide over Standard?",
                "answers": [
                    {"id": "a", "text": "Only basic email export functionality", "correct": False},
                    {"id": "b", "text": "OCR, near-duplicate detection, email threading, and custodian management", "correct": True},
                    {"id": "c", "text": "Real-time chat monitoring in Teams", "correct": False},
                    {"id": "d", "text": "Automated regulatory fine calculation", "correct": False}
                ]
            },
            {
                "question": "What is a custodian in the context of eDiscovery?",
                "answers": [
                    {"id": "a", "text": "The external legal firm handling the case", "correct": False},
                    {"id": "b", "text": "An individual whose data is relevant to an investigation and requires legal holds", "correct": True},
                    {"id": "c", "text": "The compliance officer reviewing flagged content", "correct": False},
                    {"id": "d", "text": "An automated ML model that classifies data", "correct": False}
                ]
            },
            {
                "question": "What technology does Communication Compliance use to detect policy violations in communications?",
                "answers": [
                    {"id": "a", "text": "Only manual keyword matching", "correct": False},
                    {"id": "b", "text": "ML models, trainable classifiers, and policy-based conditions", "correct": True},
                    {"id": "c", "text": "Network packet inspection", "correct": False},
                    {"id": "d", "text": "Endpoint detection and response", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "security-operations",
        "title": "Microsoft Defender XDR: Unified Security",
        "slug": "sc100-defender-xdr",
        "description": "Correlating threats across endpoints, email, identity, and cloud apps in a single unified security operations platform.",
        "hook": "Defender XDR stitches together alerts from every domain into a single incident — because attackers don't stay in one lane.",
        "problem": "Security teams drown in isolated alerts across disconnected consoles, missing the bigger picture of coordinated attacks.",
        "explanation": "Microsoft Defender XDR unifies Defender for Endpoint, Office 365, Identity, and Cloud Apps into one portal with cross-domain incident correlation. Automated Investigation and Response (AIR) triages alerts and remediates threats automatically. Advanced hunting lets you write KQL queries across all data. The unified security operations platform eliminates alert fatigue by correlating related signals into consolidated incidents.",
        "real_world_example": "An attacker compromises an email account, downloads a malicious attachment on an endpoint, and accesses cloud storage. Defender XDR correlates all three signals into one incident, auto-isolates the endpoint, and blocks the compromised account — all within minutes.",
        "summary": "Defender XDR unifies security signals across all domains into correlated incidents with automated response, dramatically reducing mean time to respond.",
        "curiosity_hook": "Defender XDR's cross-domain correlation can connect a phishing email to a lateral movement 48 hours later that no single tool would have linked.",
        "dialogue": [
            {"speaker": "Peter", "text": "Why do we need XDR when we already have separate Defender products?"},
            {"speaker": "Stewie", "text": "Because attacks span domains. XDR correlates endpoint, email, identity, and cloud signals into one picture."},
            {"speaker": "Peter", "text": "So what's the big deal about cross-domain correlation?"},
            {"speaker": "Stewie", "text": "A phishing email plus suspicious endpoint activity plus unusual cloud access. Together, it's a breach."},
            {"speaker": "Peter", "text": "What about Automated Investigation and Response?"},
            {"speaker": "Stewie", "text": "AIR triages alerts, collects evidence, and remediates threats automatically. Analysts focus on what matters."},
            {"speaker": "Peter", "text": "Can I query the data myself?"},
            {"speaker": "Stewie", "text": "Advanced hunting lets you write KQL queries across all Defender data. Full visibility, full control."},
            {"speaker": "Peter", "text": "Does it reduce alert fatigue?"},
            {"speaker": "Stewie", "text": "Dramatically. Related alerts collapse into one incident. Instead of 200 alerts, you see 5 meaningful ones."},
            {"speaker": "Peter", "text": "How does it compare to just using Sentinel alone?"},
            {"speaker": "Stewie", "text": "Sentinel is your SIEM for external data. XDR is deep Defender integration. Together, they're unstoppable."},
        ],
        "learning_objectives": [
            "Explain how Defender XDR correlates security signals across endpoint, email, identity, and cloud apps",
            "Describe Automated Investigation and Response (AIR) and its role in reducing SOC workload",
            "Understand Advanced Hunting and KQL querying across unified security data",
            "Differentiate the roles of Defender XDR and Microsoft Sentinel in the security operations stack"
        ],
        "quiz_questions": [
            {
                "question": "What is the primary benefit of cross-domain incident correlation in Defender XDR?",
                "answers": [
                    {"id": "a", "text": "Reducing the number of security products deployed", "correct": False},
                    {"id": "b", "text": "Linking related alerts across endpoints, email, identity, and cloud into a single meaningful incident", "correct": True},
                    {"id": "c", "text": "Eliminating the need for threat hunting", "correct": False},
                    {"id": "d", "text": "Automatically paying for Microsoft licensing", "correct": False}
                ]
            },
            {
                "question": "What does Automated Investigation and Response (AIR) do?",
                "answers": [
                    {"id": "a", "text": "It replaces all human analysts with AI", "correct": False},
                    {"id": "b", "text": "It triages alerts, collects evidence, and remediates threats to reduce SOC workload", "correct": True},
                    {"id": "c", "text": "It only generates reports for management review", "correct": False},
                    {"id": "d", "text": "It monitors network traffic for DDoS attacks", "correct": False}
                ]
            },
            {
                "question": "Which query language is used for Advanced Hunting in Defender XDR?",
                "answers": [
                    {"id": "a", "text": "SQL", "correct": False},
                    {"id": "b", "text": "KQL (Kusto Query Language)", "correct": True},
                    {"id": "c", "text": "SPL (Search Processing Language)", "correct": False},
                    {"id": "d", "text": "Python", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "security-operations",
        "title": "Microsoft Sentinel: Cloud-Native SIEM",
        "slug": "sc100-sentinel-siem",
        "description": "Building a cloud-native SIEM with Sentinel's data connectors, analytics rules, workbooks, and threat intelligence.",
        "hook": "Sentinel is your cloud-native security brain — ingesting everything, correlating anything, and responding automatically.",
        "problem": "Legacy SIEMs are expensive, slow, and can't scale to cloud data volumes. Modern SOC needs cloud-native elasticity.",
        "explanation": "Microsoft Sentinel sits on Log Analytics workspaces and ingests data via connectors for M365, Azure, AWS, GCP, syslog, and CEF. Analytics rules range from scheduled queries to near-real-time alerts, fusion ML for multi-stage attacks, and anomaly detection. Incidents are auto-created from alerts. Workbooks visualize trends, watchlists add context, and the content hub provides ready-made detection templates. RBAC controls access at workspace and resource levels.",
        "real_world_example": "A mid-size company connects M365, Azure AD, and AWS CloudTrail to Sentinel. A fusion rule correlates a suspicious login from AWS with an anomalous M365 file download, surfacing a multi-stage attack that single-source monitoring would miss.",
        "summary": "Sentinel provides cloud-native SIEM with elastic scalability, rich data connectors, advanced analytics, and integrated threat intelligence.",
        "curiosity_hook": "Sentinel's fusion engine can automatically correlate up to 10 low-fidelity alerts into a single high-fidelity incident using ML — detecting attacks no rule could catch.",
        "dialogue": [
            {"speaker": "Peter", "text": "Why is Sentinel called cloud-native? What makes it different?"},
            {"speaker": "Stewie", "text": "It runs entirely in Azure. No hardware to maintain, scales on demand, pay for what you ingest."},
            {"speaker": "Peter", "text": "What data connectors are available?"},
            {"speaker": "Stewie", "text": "Microsoft 365, Azure services, AWS, GCP, syslog, CEF, and hundreds of third-party connectors."},
            {"speaker": "Peter", "text": "How do analytics rules work?"},
            {"speaker": "Stewie", "text": "Scheduled rules run KQL queries on intervals. Fusion rules use ML to correlate multiple low-confidence signals."},
            {"speaker": "Peter", "text": "What's a fusion rule exactly?"},
            {"speaker": "Stewie", "text": "It correlates related alerts into a single high-fidelity incident. Detects multi-stage attacks."},
            {"speaker": "Peter", "text": "And workbooks?"},
            {"speaker": "Stewie", "text": "Visual dashboards showing trends, metrics, and investigation views across your security data."},
            {"speaker": "Peter", "text": "How do I control who sees what in Sentinel?"},
            {"speaker": "Stewie", "text": "RBAC at the workspace level. Restrict access to specific tables, actions, or data ranges."},
        ],
        "learning_objectives": [
            "Explain Log Analytics workspace design and data connector options in Microsoft Sentinel",
            "Differentiate between scheduled, near-real-time, and fusion analytics rules",
            "Describe incident creation, workbooks, and watchlists for SOC operations",
            "Understand RBAC, workspace sizing, and the role of threat intelligence in Sentinel"
        ],
        "quiz_questions": [
            {
                "question": "What does Sentinel's fusion engine do that scheduled analytics rules cannot?",
                "answers": [
                    {"id": "a", "text": "Run KQL queries on a fixed schedule", "correct": False},
                    {"id": "b", "text": "Automatically correlate multiple low-confidence signals into a high-fidelity incident using ML", "correct": True},
                    {"id": "c", "text": "Ingest data from AWS CloudTrail", "correct": False},
                    {"id": "d", "text": "Generate compliance reports for auditors", "correct": False}
                ]
            },
            {
                "question": "What is the purpose of watchlists in Microsoft Sentinel?",
                "answers": [
                    {"id": "a", "text": "To store analytics rule definitions", "correct": False},
                    {"id": "b", "text": "To upload custom data like VIP users or known bad IPs for enriching investigations", "correct": True},
                    {"id": "c", "text": "To manage user authentication for the SOC team", "correct": False},
                    {"id": "d", "text": "To schedule automatic workspace backups", "correct": False}
                ]
            },
            {
                "question": "Which data connector would you use to ingest AWS activity logs into Sentinel?",
                "answers": [
                    {"id": "a", "text": "Syslog connector", "correct": False},
                    {"id": "b", "text": "CEF connector", "correct": False},
                    {"id": "c", "text": "AWS CloudTrail connector", "correct": True},
                    {"id": "d", "text": "Windows Event Log connector", "correct": False}
                ]
            }
        ]
    },
    {
        "concept_slug": "security-operations",
        "title": "SOC Operations & Threat Hunting",
        "slug": "sc100-soc-operations",
        "description": "Building an effective SOC with team structures, maturity models, threat hunting, and automated response playbooks.",
        "hook": "A SOC without threat hunting is just a reaction team. Proactive hunting turns defenders into attackers.",
        "problem": "Most SOCs are drowning in alerts and only respond after damage is done. Proactive operations flip the script.",
        "explanation": "SOC structure includes blue team (defense), red team (offense), and purple team (collaboration). Maturity is measured against CMMI levels from initial to optimizing. Threat hunting uses KQL and MITRE ATT&CK mapping to proactively search for threats. Automated response playbooks built in Logic Apps execute responses at machine speed. Detection engineering creates, tests, and refines detection rules. Threat intelligence integration feeds external context into hunts.",
        "real_world_example": "A purple team exercises a ransomware scenario. The red team simulates initial access and lateral movement while the blue team tests detections. Gaps are identified and new KQL analytics rules are deployed within a week.",
        "summary": "An effective SOC combines structured teams, maturity frameworks, proactive hunting, and automated playbooks to stay ahead of attackers.",
        "curiosity_hook": "The MITRE ATT&CK framework has over 200 techniques. Most organizations detect fewer than 30%. Threat hunting closes that gap.",
        "dialogue": [
            {"speaker": "Peter", "text": "What's the difference between blue team, red team, and purple team?"},
            {"speaker": "Stewie", "text": "Blue defends, red attacks, purple is both working together. Purple teaming makes both sides better."},
            {"speaker": "Peter", "text": "What's a SOC maturity model?"},
            {"speaker": "Stewie", "text": "CMMI-based levels from initial chaos to optimized automation. Measures how sophisticated your ops are."},
            {"speaker": "Peter", "text": "How does threat hunting actually work?"},
            {"speaker": "Stewie", "text": "You form a hypothesis based on threat intel, write KQL queries, and proactively search for compromise."},
            {"speaker": "Peter", "text": "What's MITRE ATT&CK?"},
            {"speaker": "Stewie", "text": "A knowledge base of attacker techniques and tactics. Maps how attacks happen so you build detections."},
            {"speaker": "Peter", "text": "What about playbooks? Are those just runbooks?"},
            {"speaker": "Stewie", "text": "Automated playbooks in Logic Apps execute response actions at machine speed. Isolate, disable, notify."},
            {"speaker": "Peter", "text": "What's detection engineering?"},
            {"speaker": "Stewie", "text": "The practice of creating, testing, and maintaining detection rules. It's engineering, not just tuning."},
        ],
        "learning_objectives": [
            "Describe SOC team structures including blue, red, and purple team roles",
            "Explain SOC maturity models based on CMMI levels and their practical application",
            "Understand threat hunting methodology using KQL, MITRE ATT&CK, and hypothesis-driven approaches",
            "Describe automated response playbooks using Logic Apps and their integration with detection engineering"
        ],
        "quiz_questions": [
            {
                "question": "What is the role of a purple team in SOC operations?",
                "answers": [
                    {"id": "a", "text": "Only conducting penetration tests", "correct": False},
                    {"id": "b", "text": "Collaborating between offensive and defensive teams to improve detection and response", "correct": True},
                    {"id": "c", "text": "Managing compliance audits and reporting", "correct": False},
                    {"id": "d", "text": "Building and maintaining the SOC infrastructure", "correct": False}
                ]
            },
            {
                "question": "How do automated response playbooks in Logic Apps help SOC operations?",
                "answers": [
                    {"id": "a", "text": "They replace the need for threat hunting entirely", "correct": False},
                    {"id": "b", "text": "They execute response actions like isolating endpoints at machine speed", "correct": True},
                    {"id": "c", "text": "They generate compliance reports for auditors", "correct": False},
                    {"id": "d", "text": "They manage user access provisioning in Entra ID", "correct": False}
                ]
            },
            {
                "question": "What framework maps attacker techniques and tactics for use in threat hunting and detection engineering?",
                "answers": [
                    {"id": "a", "text": "NIST Cybersecurity Framework", "correct": False},
                    {"id": "b", "text": "ISO 27001", "correct": False},
                    {"id": "c", "text": "MITRE ATT&CK", "correct": True},
                    {"id": "d", "text": "CIS Controls", "correct": False}
                ]
            }
        ]
    },
]
LESSONS = rewrite_lessons_dialogues(LESSONS)
