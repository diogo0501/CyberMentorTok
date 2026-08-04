ROADMAP_SOURCE_URL = "https://pwnedlabs.io/resources/cloud-security-engineer-roadmap"
ROADMAP_PDF_URL = "https://pwnedlabs.io/hubfs/Cloud%20Security%20Engineer%20Roadmap%20by%20Pwned%20Labs.pdf"


ROADMAP_LESSONS = [
    {
        "id": "plr-001",
        "title": "Linux for Cloud Security: Processes, Permissions, and Operational Reality",
        "concept": "linux-foundations",
        "category": "roadmap-foundation",
        "difficulty": 1,
        "media_id": "2475649c",
        "hook": "Cloud security engineers live in abstractions until an incident drags them back down to the operating system.",
        "description": "A beginner-to-intermediate lesson on Linux essentials that actually matter for cloud security work.",
        "problem": "People jump straight into cloud consoles without understanding the host concepts underneath: users, groups, processes, sockets, filesystems, and permissions.",
        "explanation": "Linux fluency matters because cloud workloads, containers, CI runners, and incident response all eventually reduce to operating-system behavior. Experts expect familiarity with process trees, privilege boundaries, service managers, network listeners, file ownership, ACLs, and shell automation because these explain how cloud misconfigurations turn into concrete exposure. Even when a provider abstracts the infrastructure, the workload still inherits OS realities such as credential files, package drift, weak daemon hardening, and insecure permissions.",
        "summary": "Cloud security starts higher up, but real debugging and compromise paths still terminate in Linux behavior."
    },
    {
        "id": "plr-002",
        "title": "Containers for Beginners: Namespaces, Images, and Why Isolation Is Not Magic",
        "concept": "container-basics",
        "category": "roadmap-foundation",
        "difficulty": 1,
        "media_id": "971a67b8",
        "hook": "Containers feel simple because packaging is simple. Isolation and trust are the hard parts hidden underneath.",
        "description": "A foundations lesson on what containers are, how they differ from VMs, and why cloud defenders need to care.",
        "problem": "Beginners treat containers as tiny virtual machines and miss the shared-kernel assumptions that matter for security and operations.",
        "explanation": "Containers package processes with filesystem, namespace, and runtime isolation primitives, but they do not create full hardware-level separation. Experts care about image provenance, privilege flags, syscall exposure, mounted secrets, and orchestrator policy because those define the real security posture. Container literacy is foundational since many cloud-native workloads, CI systems, and attack paths depend on understanding this packaging and isolation model.",
        "summary": "Learn containers as a process-isolation and packaging model, not as magic mini-servers."
    },
    {
        "id": "plr-003",
        "title": "Choose One Cloud First: Why Depth Beats Multi-Cloud Shallowness",
        "concept": "one-cloud-provider",
        "category": "roadmap-foundation",
        "difficulty": 1,
        "media_id": "d91ed72a",
        "hook": "A cloud security career usually begins faster when one provider becomes second nature before three providers become confusing.",
        "description": "Why the roadmap starts with one cloud provider and how deep provider fluency accelerates later security learning.",
        "problem": "Beginners spread attention across AWS, Azure, and GCP too early, never building the mental model required to spot dangerous provider-specific mistakes.",
        "explanation": "Each cloud provider has its own identity fabric, networking model, storage semantics, audit layers, and control-plane assumptions. Experts know that real mistakes happen inside those provider-specific details, not in generic cloud buzzwords. Starting with one provider creates depth in terminology, service relationships, and hands-on troubleshooting, which later transfers into stronger multi-cloud reasoning. Breadth without depth often produces certification vocabulary but not defensive capability.",
        "summary": "Go deep in one provider first. Security insight comes from concrete provider mechanics, not generic multi-cloud familiarity."
    },
    {
        "id": "plr-004",
        "title": "Shared Responsibility in Practice: Where Provider Security Ends and Yours Begins",
        "concept": "shared-responsibility-practice",
        "category": "roadmap-foundation",
        "difficulty": 1,
        "media_id": "5925bf59",
        "hook": "The shared responsibility model is simple to memorize and surprisingly easy to misunderstand in real systems.",
        "description": "A beginner lesson on translating the shared responsibility model into practical security ownership.",
        "problem": "Teams think a managed cloud service means the provider handles security end to end, then miss their own duties around identity, configuration, and data protection.",
        "explanation": "Providers secure the cloud's foundational layers, but customers still control access, network exposure, secrets, data classification, logging choices, and workload code. Experts go further by mapping responsibility at service granularity because a serverless database, a VM, and a SaaS identity integration each split duties differently. The shared responsibility model becomes useful only when translated into precise ownership statements and operational checks.",
        "summary": "Know exactly what the provider secures, what you still configure, and how that answer changes by service type."
    },
    {
        "id": "plr-005",
        "title": "Cloud Security Principles: Least Privilege, Defense in Depth, and Explicit Trust",
        "concept": "cloud-security-principles",
        "category": "roadmap-foundation",
        "difficulty": 1,
        "media_id": "06f1eef0",
        "hook": "Before tools, services, or certifications, cloud security is a set of design principles that explain what good looks like.",
        "description": "A dense foundations lesson on the core principles that recur across every cloud security domain.",
        "problem": "Beginners learn controls one by one but never connect them to deeper principles, so they struggle to reason when the environment changes.",
        "explanation": "Cloud security principles include least privilege, explicit trust verification, immutable infrastructure bias, separation of duties, defense in depth, and observability as a safety property. Experts use principles as compression: they let you evaluate unfamiliar services quickly because you can ask how identity is scoped, how blast radius is bounded, where monitoring exists, and what happens during failure. Principles turn cloud security from memorization into judgment.",
        "summary": "Principles are the mental model that make cloud security transferable across providers and technologies."
    },
    {
        "id": "plr-006",
        "title": "The Hacker Mindset for Defenders: Thinking in Paths, Not Products",
        "concept": "hacker-mindset",
        "category": "roadmap-foundation",
        "difficulty": 2,
        "media_id": "f3ef33f4",
        "hook": "Attackers do not care which tool category you bought. They care which path gets them from weak point to valuable outcome.",
        "description": "A roadmap lesson on attacker thinking for cloud defenders: chaining weaknesses, abusing trust, and following permissions.",
        "problem": "Defenders often think in isolated controls, while attackers think in sequences of opportunities that compound each other.",
        "explanation": "The hacker mindset is about pathfinding. A low-severity metadata exposure, an over-broad role, and a neglected logging gap may combine into a full account compromise. Experts train themselves to think in attack graphs, credential movement, control bypasses, and business impact rather than only in single misconfigurations. This mindset improves architecture review, threat modeling, and incident triage because it emphasizes how local weaknesses become systemic breaches.",
        "summary": "Think like an attacker by tracing how small trust failures compose into real access and real damage."
    },
    {
        "id": "plr-007",
        "title": "Scripting for Security Engineers: Automating Boring Checks Without Becoming Fragile",
        "concept": "security-automation-basics",
        "category": "roadmap-foundation",
        "difficulty": 2,
        "media_id": "8c06f258",
        "hook": "Automation is how security work scales, but weak automation can spread bad assumptions just as fast.",
        "description": "A practical lesson on why scripting matters for cloud security engineers and what kinds of tasks it should handle first.",
        "problem": "Manual reviews do not scale across accounts, policies, buckets, logs, and findings, but beginners often over-automate before understanding the signal.",
        "explanation": "Security engineers script inventory collection, policy checks, key rotation audits, log parsing, and evidence gathering long before they build complex platforms. Experts keep automation narrow, observable, and testable at first, because brittle scripts with broad permissions can create silent operational risk. Good automation removes repetitive toil while making assumptions explicit and reviewable.",
        "summary": "Automate repetitive inspection first. Scale signal, not confusion."
    },
    {
        "id": "plr-008",
        "title": "IAM Foundations: Principals, Policies, and Effective Permissions",
        "concept": "iam-foundations",
        "category": "roadmap-core",
        "difficulty": 2,
        "media_id": "cac4f7d2",
        "hook": "In cloud security, the most important network boundary is often the permission graph.",
        "description": "A deeper beginner lesson on identities, roles, groups, policies, inheritance, and why effective permission is the real question.",
        "problem": "People read one policy in isolation and think they understand access, while the real permission outcome is produced by many overlapping layers.",
        "explanation": "IAM starts with principals such as users, services, and workloads, but the important step is evaluating effective permission after all attached policies, conditions, groups, boundaries, and resource policies combine. Experts also care about assumption paths: who can impersonate whom, who can create new credentials, and who can attach stronger policy than they currently hold. IAM is foundational because almost every serious cloud breach involves identity misuse somewhere in the chain.",
        "summary": "Do not ask only what a policy says. Ask what a principal can effectively do after every path and condition is applied."
    },
    {
        "id": "plr-009",
        "title": "IAM Evaluation Logic: Explicit Deny, Resource Policy, and Permission Boundaries",
        "concept": "iam-evaluation-logic",
        "category": "roadmap-core",
        "difficulty": 3,
        "media_id": "81bb67f2",
        "hook": "Access control mistakes happen when engineers reason about one policy document instead of the full evaluation engine.",
        "description": "A denser IAM lesson on how cloud providers evaluate multiple policy types and why boundaries matter.",
        "problem": "Security teams misdiagnose access because they do not model the interaction between identity policy, resource policy, SCPs, permission boundaries, and explicit deny.",
        "explanation": "Effective permission is an evaluation problem, not a reading problem. Experts understand precedence rules: explicit deny wins, some policy types intersect while others union, and boundaries or org-level guardrails can narrow what identity policy otherwise permits. This matters operationally because debugging access and proving least privilege both require an accurate mental model of the evaluator, not just the documents stored in the console.",
        "summary": "Learn the evaluator, not only the syntax. Cloud IAM is an engine with precedence, not a pile of JSON."
    },
    {
        "id": "plr-010",
        "title": "Privilege Escalation in the Cloud: How Small Permissions Become Big Ones",
        "concept": "cloud-privilege-escalation",
        "category": "roadmap-core",
        "difficulty": 3,
        "media_id": "81bb67f2",
        "hook": "Many dangerous cloud permissions do not look like admin until they are chained with one more action.",
        "description": "A denser IAM lesson on escalation paths through role assumption, policy attachment, pass-role rights, and service abuse.",
        "problem": "Organizations review identities for obvious admin rights but miss the indirect paths that still let attackers mint stronger access.",
        "explanation": "Cloud privilege escalation usually exploits meta-permissions: creating credentials, attaching policies, passing high-privilege roles to services, editing trust policies, or triggering managed services under stronger identities. Experts map these paths continuously because modern attackers do not need one giant admin policy if they can synthesize equivalent power through control-plane steps. Least privilege therefore means constraining capability graphs, not just removing the word admin.",
        "summary": "Escalation risk lives in what identities can become, not just in what they are today."
    },
    {
        "id": "plr-011",
        "title": "Network Security Basics: VPCs, Subnets, Routes, and Reachability",
        "concept": "cloud-network-basics",
        "category": "roadmap-core",
        "difficulty": 2,
        "media_id": "aeb6c556",
        "hook": "Cloud networking feels abstract until you realize every exposure is just reachability plus trust.",
        "description": "A beginner-to-intermediate lesson on the cloud network constructs every security engineer must understand.",
        "problem": "People memorize terms like VPC and subnet without understanding how routes, gateways, and filters together decide whether traffic can reach anything useful.",
        "explanation": "Cloud network security begins with address space, subnet purpose, route tables, internet or NAT gateways, private connectivity, and stateful or stateless filtering layers. Experts think in reachability graphs: from where, to what, through which routes, under which identity or protocol assumptions. This makes it possible to reason about attack surface, segmentation, exfiltration, and incident containment at a provider-native level.",
        "summary": "Cloud networking is security when you can explain who can reach what, by which path, and why."
    },
    {
        "id": "plr-012",
        "title": "Cloud Firewalls and Microsegmentation",
        "concept": "cloud-microsegmentation",
        "category": "roadmap-core",
        "difficulty": 3,
        "media_id": "6ba9aed4",
        "hook": "Segmentation in the cloud is less about perimeter walls and more about shrinking lateral movement options.",
        "description": "A dense network lesson on security groups, network ACLs, service mesh policy, and workload-level segmentation.",
        "problem": "Teams recreate flat internal networks in the cloud, assuming the external edge matters most while east-west exposure remains broad.",
        "explanation": "Microsegmentation in cloud environments combines provider-native controls, workload identity, private endpoints, and sometimes service-mesh authorization. Experts avoid broad internal trust by scoping who may talk to whom, on which ports, under which service identity, and with what observability. Good segmentation should remain understandable during incidents and should not be so complex that operators disable it under pressure.",
        "summary": "Cloud segmentation is about enforcing least privilege for service-to-service traffic, not just hardening the public edge."
    },
    {
        "id": "plr-013",
        "title": "Encryption Basics for Cloud Engineers: At Rest, In Transit, and In Use",
        "concept": "cloud-encryption-basics",
        "category": "roadmap-core",
        "difficulty": 2,
        "media_id": "e2a3cee0",
        "hook": "Encryption becomes useful only when you know exactly what threat it addresses and what it does not.",
        "description": "A dense fundamentals lesson on encryption states and the architecture decisions behind each one.",
        "problem": "Beginners hear 'encrypted' and assume data is universally safe, without asking from whom, at what moment, and under whose key control.",
        "explanation": "Encryption at rest protects stored media and snapshots, encryption in transit protects data crossing untrusted paths, and encryption in use is a more specialized concern involving memory exposure and confidential compute models. Experts care about where keys live, who can request decrypt, how logs expose plaintext, and whether provider-managed defaults satisfy the organization's trust model. The security value of encryption depends on key architecture, access paths, and operational practices.",
        "summary": "Always ask what is encrypted, when, under whose keys, and against which threat."
    },
    {
        "id": "plr-014",
        "title": "Storage Security: Buckets, Snapshots, and Data Exposure Patterns",
        "concept": "storage-security-patterns",
        "category": "roadmap-core",
        "difficulty": 2,
        "media_id": "2ae00c90",
        "hook": "Storage breaches are often boring in mechanism and catastrophic in impact.",
        "description": "A roadmap lesson on cloud storage security from object stores to disks, snapshots, and managed databases.",
        "problem": "Teams focus on compute while data leaks happen through public buckets, permissive sharing, exposed snapshots, and over-broad access paths.",
        "explanation": "Storage security requires understanding object policies, block snapshot exposure, replica access, lifecycle rules, encryption settings, and audit trails for reads and writes. Experts also look at cross-account sharing, backup inheritance, data residency, and whether non-production copies quietly bypass production controls. The cloud makes storage durable and easy to share; that convenience is exactly why governance must be deliberate.",
        "summary": "Data exposure often comes from storage defaults, copy paths, and sharing semantics rather than dramatic software exploits."
    },
    {
        "id": "plr-015",
        "title": "Logging Foundations: What to Turn On Before You Need It",
        "concept": "logging-foundations",
        "category": "roadmap-core",
        "difficulty": 2,
        "media_id": "d0af26de",
        "hook": "Incident response begins long before the incident, usually with one checkbox someone forgot to enable.",
        "description": "A dense foundations lesson on cloud audit logs, flow logs, workload logs, and telemetry retention strategy.",
        "problem": "Organizations try to investigate cloud events without account-level audit trails, network logs, or centralized retention, then discover the evidence never existed.",
        "explanation": "Logging foundations start with control-plane audit logs, identity events, storage access records, network flow visibility, and workload/application telemetry. Experts decide which logs are high-value, where they aggregate, how long they are retained, and who can tamper with or disable them. A logging architecture must be trustworthy under compromise, or it becomes a post-breach comfort blanket rather than evidence.",
        "summary": "Turn on the logs that explain identity, control-plane change, storage access, and network behavior before you ever need them."
    },
    {
        "id": "plr-016",
        "title": "Detection Engineering in the Cloud: From Log Collection to Useful Detections",
        "concept": "cloud-detection-engineering",
        "category": "roadmap-core",
        "difficulty": 3,
        "media_id": "10e72169",
        "hook": "Collecting logs is easy compared with deciding what suspicious cloud behavior actually looks like.",
        "description": "A denser lesson on cloud detections for IAM abuse, storage exposure, unusual regions, service misuse, and control-plane drift.",
        "problem": "Security teams ingest huge cloud telemetry streams but produce noisy detections that miss meaningful attacker behavior.",
        "explanation": "Detection engineering translates cloud attack paths into observable signals such as impossible role use, unusual API sequencing, unexpected region deployment, bursty secret access, or policy weakening. Experts care about baseline quality, field normalization, context enrichment, and which detections truly map to attacker tradecraft versus administrative variance. Strong detections are hypothesis-driven and measurable, not merely query collections.",
        "summary": "Detection quality comes from understanding cloud attacker behavior well enough to ask the telemetry specific, useful questions."
    },
    {
        "id": "plr-017",
        "title": "Cloud Incident Response: Containment Without Destroying Evidence",
        "concept": "cloud-incident-response",
        "category": "roadmap-advanced",
        "difficulty": 3,
        "media_id": "1cac313b",
        "hook": "Cloud incidents move fast because credentials, APIs, and automation can scale the attacker's reach instantly.",
        "description": "A lesson on response sequencing for cloud incidents: scoping, containment, identity control, evidence preservation, and recovery.",
        "problem": "Teams rush to shut systems down and accidentally destroy volatile evidence, sever forensic context, or break the business without containing the actual attacker path.",
        "explanation": "Cloud incident response must account for identity revocation, policy rollback, snapshot capture, log preservation, and sometimes pausing automation that would otherwise erase traces or redeploy compromised state. Experts distinguish data-plane symptoms from control-plane causes and aim to contain the attack path rather than just the loudest host. The cloud changes response because the control plane itself is often both the breach vector and the recovery lever.",
        "summary": "Respond to cloud incidents by preserving evidence, constraining attacker identity paths, and understanding control-plane state before destroying it."
    },
    {
        "id": "plr-018",
        "title": "Disaster Recovery for Cloud Security Engineers",
        "concept": "cloud-dr-foundations",
        "category": "roadmap-advanced",
        "difficulty": 3,
        "media_id": "27e2daad",
        "hook": "Recovery is part of security because attackers, accidents, and outages all test whether you can restore trustworthy service.",
        "description": "A denser lesson on backup trust, immutable recovery, region failover, and rebuilding secure state after disruption.",
        "problem": "Organizations back data up but do not know whether they can restore it safely, quickly, or without reintroducing the compromise.",
        "explanation": "Disaster recovery in cloud environments includes not only data restoration but identity recovery, network baseline restoration, key access, pipeline trust, and validation that recovered assets are not still contaminated. Experts care about immutable backups, separation between production and recovery control paths, and exercises that prove the environment can re-emerge securely. Recovery that restores compromised policy or stale keys is not a successful recovery.",
        "summary": "Disaster recovery is secure-state restoration, not just file restoration."
    },
    {
        "id": "plr-019",
        "title": "Cloud Security Posture Management: What It Solves and What It Cannot",
        "concept": "cspm-basics",
        "category": "roadmap-advanced",
        "difficulty": 3,
        "media_id": "65178cf4",
        "hook": "Posture tools are useful because cloud misconfigurations are abundant. They are dangerous when teams mistake findings for a security strategy.",
        "description": "A deeper lesson on CSPM, configuration drift, control coverage, and the gap between findings and real risk reduction.",
        "problem": "Teams deploy posture tools, close a subset of alerts, and assume the environment is secure even though identity paths, workload flaws, and business context remain poorly understood.",
        "explanation": "CSPM tools excel at continuously checking policy and configuration against known patterns: public exposure, weak logging, encryption gaps, risky identities, and missing controls. Experts use them as inventory and drift-detection engines, then layer identity reasoning, attack-path analysis, and workload-specific context on top. CSPM is powerful for breadth, but it does not replace architectural judgment, incident readiness, or deep service knowledge.",
        "summary": "Use posture tools as visibility accelerators, not as substitutes for threat reasoning and architecture understanding."
    },
    {
        "id": "plr-020",
        "title": "Attack Paths in the Cloud: From Misconfiguration to Material Impact",
        "concept": "cloud-attack-paths",
        "category": "roadmap-advanced",
        "difficulty": 4,
        "media_id": "f3ef33f4",
        "hook": "Single findings matter less than the path that connects them to privilege, data, or disruption.",
        "description": "A dense advanced lesson on attack-path thinking across IAM, storage, network, workload, and monitoring gaps.",
        "problem": "Security teams drown in isolated findings because they do not consistently model how multiple weaknesses compose into an actual compromise route.",
        "explanation": "Cloud attack paths often start with an initial foothold such as exposed credentials, weak federation, public storage, or an over-permissive workload identity. The attacker then chains privilege escalation, discovery, lateral movement, and data access through control-plane APIs or workload weaknesses. Experts prioritize remediation by path value: which combinations actually grant business-impacting capability, not which single misconfiguration looks scariest alone. This is where architecture, detection, and IAM knowledge converge.",
        "summary": "Risk is best understood as reachable outcome through chained weakness, not as a flat list of findings."
    },
    {
        "id": "plr-021",
        "title": "Hands-On Learning Architecture: Why Labs Matter More Than Passive Study",
        "concept": "hands-on-learning",
        "category": "roadmap-meta",
        "difficulty": 1,
        "media_id": "06f1eef0",
        "hook": "Cloud security understanding hardens when you break and fix real environments, not when you only read about them.",
        "description": "A roadmap lesson on why practical labs are central to learning cloud security from beginner to expert.",
        "problem": "Passive learners build vocabulary but often cannot debug permissions, validate network paths, or explain what an attack actually looks like in telemetry.",
        "explanation": "Hands-on work turns abstract cloud concepts into operational memory. Experts improve faster by creating buckets, breaking policies, testing role assumptions, enabling logs, and observing how cloud APIs express these decisions in the real world. Labs also teach failure handling, syntax nuance, and provider-specific behavior that books rarely capture well. Practical repetition is what converts cloud security from theory into employable skill.",
        "summary": "Read to orient yourself, then build, break, and observe until the platform behavior becomes intuitive."
    },
    {
        "id": "plr-022",
        "title": "Beginner to Expert Sequencing: Why the Roadmap Order Matters",
        "concept": "roadmap-sequencing",
        "category": "roadmap-meta",
        "difficulty": 2,
        "media_id": "50c1e16a",
        "hook": "The order of learning matters because advanced cloud security assumes foundations you only notice when they are missing.",
        "description": "A meta-lesson on how foundational topics support advanced cloud security reasoning and why skipping steps creates blind spots.",
        "problem": "Learners chase advanced attack paths or specialized tools without network, IAM, or Linux fluency, then cannot explain what their tools are actually showing them.",
        "explanation": "A roadmap is not bureaucracy; it is dependency management for learning. Linux and containers explain workloads, one provider explains the platform, security principles explain judgment, automation explains scale, IAM explains the perimeter, networking explains reachability, encryption explains data protection, logging explains evidence, and incident response explains recovery. Experts move fluidly because these layers reinforce each other. Skipping too many of them creates a brittle understanding that breaks under real incidents.",
        "summary": "Sequence matters because cloud security expertise is cumulative. Each layer makes the next one intelligible."
    },
]


def build_roadmap_lessons(base_items):
    base_by_id = {item["id"]: item for item in base_items}
    max_updated = max((item.get("updated_at") or 0) for item in base_items) if base_items else 0
    extras = []

    for index, seed in enumerate(ROADMAP_LESSONS, start=1):
        media = base_by_id.get(seed["media_id"])
        if not media:
            continue
        extras.append(
            {
                "id": seed["id"],
                "title": seed["title"],
                "hook": seed["hook"],
                "description": seed["description"],
                "problem": seed["problem"],
                "explanation": seed["explanation"],
                "summary": seed["summary"],
                "lesson_id": seed["id"],
                "concept_id": seed["concept"],
                "concept": seed["concept"],
                "category": seed["category"],
                "difficulty": seed["difficulty"],
                "mask_url": media.get("mask_url"),
                "audio_url": media.get("audio_url"),
                "full_url": media.get("full_url"),
                "timing_url": media.get("timing_url"),
                "background_url": media.get("background_url"),
                "background_options": media.get("background_options"),
                "updated_at": max_updated + 3000 + index,
                "size_bytes": media.get("size_bytes"),
                "source_repo": ROADMAP_SOURCE_URL,
                "source_pdf": ROADMAP_PDF_URL,
                "source_media_id": seed["media_id"],
            }
        )

    return extras
