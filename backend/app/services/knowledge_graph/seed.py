from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.concept import Concept, ConceptPrerequisite


CONCEPTS_SEED = [
    {"name": "Binary & Data Representation", "slug": "binary", "category": "fundamentals", "difficulty": 1, "domain": "computer-science", "tags": ["binary", "hex", "data"]},
    {"name": "CPU Architecture", "slug": "cpu", "category": "fundamentals", "difficulty": 1, "domain": "computer-science", "tags": ["cpu", "processor", "architecture"]},
    {"name": "RAM & Memory", "slug": "ram", "category": "fundamentals", "difficulty": 1, "domain": "computer-science", "tags": ["memory", "ram", "volatile"]},
    {"name": "Storage Systems", "slug": "storage", "category": "fundamentals", "difficulty": 1, "domain": "computer-science", "tags": ["storage", "hdd", "ssd"]},
    {"name": "Processes & Threads", "slug": "processes", "category": "fundamentals", "difficulty": 1, "domain": "computer-science", "tags": ["process", "thread", "scheduling"]},
    {"name": "Operating Systems", "slug": "operating-systems", "category": "fundamentals", "difficulty": 1, "domain": "computer-science", "tags": ["os", "kernel", "system"]},
    {"name": "Networking Fundamentals", "slug": "networking", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["network", "basics"]},
    {"name": "Ethernet & MAC", "slug": "ethernet", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["ethernet", "mac", "layer2"]},
    {"name": "OSI Model", "slug": "osi-model", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["osi", "layers", "model"]},
    {"name": "TCP/IP", "slug": "tcp-ip", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["tcp", "ip", "protocol"]},
    {"name": "IP Addressing", "slug": "ip-addressing", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["ip", "address", "subnet"]},
    {"name": "DNS", "slug": "dns", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["dns", "domain", "resolution"]},
    {"name": "HTTP & HTTPS", "slug": "http-https", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["http", "https", "web"]},
    {"name": "TLS/SSL", "slug": "tls-ssl", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["tls", "ssl", "encryption"]},
    {"name": "Ports & Sockets", "slug": "ports-sockets", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["ports", "sockets", "transport"]},
    {"name": "Routing & Switching", "slug": "routing-switching", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["routing", "switching", "router"]},
    {"name": "NAT", "slug": "nat", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["nat", "translation", "firewall"]},
    {"name": "VPN", "slug": "vpn", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["vpn", "tunnel", "encryption"]},
    {"name": "Firewalls", "slug": "firewalls", "category": "networking", "difficulty": 2, "domain": "networking", "tags": ["firewall", "filter", "security"]},
    {"name": "IPv6", "slug": "ipv6", "category": "networking", "difficulty": 3, "domain": "networking", "tags": ["ipv6", "address", "next-gen"]},
    {"name": "Linux Fundamentals", "slug": "linux", "category": "linux", "difficulty": 3, "domain": "operating-systems", "tags": ["linux", "unix", "cli"]},
    {"name": "Linux Filesystem", "slug": "linux-filesystem", "category": "linux", "difficulty": 3, "domain": "operating-systems", "tags": ["filesystem", "hierarchy", "fhs"]},
    {"name": "Linux Permissions", "slug": "linux-permissions", "category": "linux", "difficulty": 3, "domain": "operating-systems", "tags": ["permissions", "chmod", "ownership"]},
    {"name": "Bash Scripting", "slug": "bash", "category": "linux", "difficulty": 3, "domain": "operating-systems", "tags": ["bash", "shell", "scripting"]},
    {"name": "SSH", "slug": "ssh", "category": "linux", "difficulty": 3, "domain": "operating-systems", "tags": ["ssh", "remote", "key"]},
    {"name": "Systemd & Services", "slug": "systemd", "category": "linux", "difficulty": 3, "domain": "operating-systems", "tags": ["systemd", "services", "init"]},
    {"name": "Windows Internals", "slug": "windows-internals", "category": "windows", "difficulty": 3, "domain": "operating-systems", "tags": ["windows", "registry", "internals"]},
    {"name": "Active Directory", "slug": "active-directory", "category": "windows", "difficulty": 4, "domain": "windows-services", "tags": ["ad", "ldap", "domain"]},
    {"name": "Kerberos", "slug": "kerberos", "category": "windows", "difficulty": 4, "domain": "windows-services", "tags": ["kerberos", "authentication", "tickets"]},
    {"name": "PowerShell", "slug": "powershell", "category": "windows", "difficulty": 3, "domain": "operating-systems", "tags": ["powershell", "scripting", "automation"]},
    {"name": "Python for Security", "slug": "python", "category": "programming", "difficulty": 3, "domain": "programming", "tags": ["python", "scripting", "automation"]},
    {"name": "CIA Triad", "slug": "cia-triad", "category": "security-fundamentals", "difficulty": 2, "domain": "security", "tags": ["cia", "confidentiality", "integrity"]},
    {"name": "Threats & Vulnerabilities", "slug": "threats-vulnerabilities", "category": "security-fundamentals", "difficulty": 2, "domain": "security", "tags": ["threats", "vulnerabilities", "weakness"]},
    {"name": "OWASP Top 10", "slug": "owasp", "category": "security-fundamentals", "difficulty": 3, "domain": "web-security", "tags": ["owasp", "web", "injection"]},
    {"name": "MITRE ATT&CK", "slug": "mitre-attack", "category": "security-fundamentals", "difficulty": 3, "domain": "security", "tags": ["mitre", "attack", "framework"]},
    {"name": "SIEM", "slug": "siem", "category": "blue-team", "difficulty": 4, "domain": "defensive", "tags": ["siem", "log", "monitoring"]},
    {"name": "EDR", "slug": "edr", "category": "blue-team", "difficulty": 4, "domain": "defensive", "tags": ["edr", "endpoint", "detection"]},
    {"name": "Incident Response", "slug": "incident-response", "category": "blue-team", "difficulty": 4, "domain": "defensive", "tags": ["ir", "response", "forensics"]},
    {"name": "Reconnaissance", "slug": "recon", "category": "red-team", "difficulty": 3, "domain": "offensive", "tags": ["recon", "osint", "passive"]},
    {"name": "Scanning & Enumeration", "slug": "scanning", "category": "red-team", "difficulty": 3, "domain": "offensive", "tags": ["nmap", "scan", "enumerate"]},
    {"name": "Exploitation", "slug": "exploitation", "category": "red-team", "difficulty": 4, "domain": "offensive", "tags": ["exploit", "metasploit", "vuln"]},
    {"name": "Privilege Escalation", "slug": "priv-esc", "category": "red-team", "difficulty": 4, "domain": "offensive", "tags": ["privesc", "sudo", "suid"]},
    {"name": "AWS Security", "slug": "aws-security", "category": "cloud", "difficulty": 4, "domain": "cloud", "tags": ["aws", "cloud", "iam"]},
    {"name": "Container Security", "slug": "container-security", "category": "cloud", "difficulty": 4, "domain": "cloud", "tags": ["docker", "container", "security"]},
    {"name": "Reverse Engineering", "slug": "reverse-engineering", "category": "advanced", "difficulty": 5, "domain": "advanced", "tags": ["reverse", "ida", "ghidra"]},
    {"name": "Malware Analysis", "slug": "malware-analysis", "category": "advanced", "difficulty": 5, "domain": "advanced", "tags": ["malware", "analysis", "sandbox"]},
    {"name": "Exploit Development", "slug": "exploit-dev", "category": "advanced", "difficulty": 6, "domain": "advanced", "tags": ["exploit", "rop", "shellcode"]},
    {"name": "Zero Trust Architecture", "slug": "zero-trust", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["zero-trust", "never-trust", "verify"]},
    {"name": "Cloud Security Frameworks", "slug": "cloud-frameworks", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["caf", "waf", "mcra", "mcsb"]},
    {"name": "Business Resilience", "slug": "resilience", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["bcr", "disaster-recovery", "backup"]},
    {"name": "Compliance & GRC", "slug": "compliance", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["compliance", "grc", "purview"]},
    {"name": "Identity & Access Management", "slug": "identity-access", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["entra-id", "conditional-access", "mfa"]},
    {"name": "Privileged Access Management", "slug": "privileged-access", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["pim", "paw", "jit", "jea"]},
    {"name": "Security Operations Architecture", "slug": "security-operations", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["soc", "xdr", "sentinel"]},
    {"name": "Application Security Architecture", "slug": "app-security-arch", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["sdl", "threat-model", "secure-coding"]},
    {"name": "Data Security & Protection", "slug": "data-security", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["encryption", "dlp", "classification"]},
    {"name": "Workload Identity Security", "slug": "workload-identity", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["managed-identity", "service-principal"]},
    {"name": "AI Security", "slug": "ai-security", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["ai", "ml", "llm", "prompt-injection"]},
    {"name": "DevSecOps Architecture", "slug": "devsecops-arch", "category": "security-architecture", "difficulty": 5, "domain": "security-architecture", "tags": ["devsecops", "iac", "supply-chain"]},
    {"name": "Cryptography Fundamentals", "slug": "cryptography", "category": "security-fundamentals", "difficulty": 3, "domain": "security", "tags": ["crypto", "encryption", "hashing"]},
    {"name": "Social Engineering", "slug": "social-engineering", "category": "security-fundamentals", "difficulty": 2, "domain": "security", "tags": ["social-engineering", "phishing", "human"]},
    {"name": "Digital Forensics", "slug": "forensics", "category": "blue-team", "difficulty": 4, "domain": "defensive", "tags": ["forensics", "evidence", "investigation"]},
    {"name": "Threat Intelligence", "slug": "threat-intelligence", "category": "blue-team", "difficulty": 4, "domain": "defensive", "tags": ["threat-intel", "ioc", "ttp"]},
    {"name": "Risk Management", "slug": "risk-management", "category": "security-fundamentals", "difficulty": 3, "domain": "security", "tags": ["risk", "framework", "compliance"]},
    {"name": "Security Awareness", "slug": "security-awareness", "category": "security-fundamentals", "difficulty": 2, "domain": "security", "tags": ["awareness", "training", "culture"]},
]

PREREQUISITES_SEED = [
    ("binary", "cpu", True), ("binary", "ram", True), ("binary", "storage", True),
    ("cpu", "processes", True), ("ram", "processes", True), ("processes", "operating-systems", True),
    ("operating-systems", "networking", True), ("networking", "osi-model", True), ("networking", "ethernet", True),
    ("osi-model", "tcp-ip", True), ("tcp-ip", "ip-addressing", True), ("tcp-ip", "ports-sockets", True),
    ("tcp-ip", "dns", True), ("tcp-ip", "http-https", True), ("http-https", "tls-ssl", True),
    ("ip-addressing", "routing-switching", True), ("ip-addressing", "nat", True),
    ("routing-switching", "firewalls", True), ("tcp-ip", "vpn", True),
    ("operating-systems", "linux", True), ("linux", "linux-filesystem", True),
    ("linux", "linux-permissions", True), ("linux", "bash", True), ("linux", "ssh", True),
    ("linux", "systemd", True), ("operating-systems", "windows-internals", True),
    ("windows-internals", "active-directory", True), ("active-directory", "kerberos", True),
    ("windows-internals", "powershell", True), ("operating-systems", "python", True),
    ("networking", "cia-triad", True), ("networking", "threats-vulnerabilities", True),
    ("http-https", "owasp", True), ("threats-vulnerabilities", "mitre-attack", True),
    ("linux", "siem", True), ("siem", "edr", True), ("siem", "incident-response", True),
    ("networking", "recon", True), ("recon", "scanning", True), ("scanning", "exploitation", True),
    ("exploitation", "priv-esc", True),
    ("linux", "aws-security", True), ("linux", "container-security", True),
    ("operating-systems", "reverse-engineering", True), ("reverse-engineering", "malware-analysis", True),
    ("operating-systems", "exploit-dev", True),
    ("networking", "zero-trust", True), ("zero-trust", "cloud-frameworks", True),
    ("cloud-frameworks", "resilience", True), ("cloud-frameworks", "compliance", True),
    ("active-directory", "identity-access", True), ("identity-access", "privileged-access", True),
    ("siem", "security-operations", True), ("cia-triad", "data-security", True),
    ("threats-vulnerabilities", "app-security-arch", True), ("identity-access", "workload-identity", True),
    ("threats-vulnerabilities", "ai-security", True), ("container-security", "devsecops-arch", True),
    ("cia-triad", "cryptography", True), ("tls-ssl", "cryptography", True),
    ("threats-vulnerabilities", "social-engineering", True), ("social-engineering", "security-awareness", True),
    ("incident-response", "forensics", True), ("siem", "threat-intelligence", True),
    ("threat-intelligence", "risk-management", True), ("compliance", "risk-management", True),
    ("cryptography", "data-security", True),
]


async def seed_knowledge_graph(db: AsyncSession):
    existing = await db.execute(select(Concept.slug))
    existing_slugs = set(row[0] for row in existing.fetchall())

    slug_to_id = {}
    added = 0
    for concept_data in CONCEPTS_SEED:
        if concept_data["slug"] not in existing_slugs:
            concept = Concept(**concept_data, is_published=True)
            db.add(concept)
            await db.flush()
            slug_to_id[concept.slug] = concept.id
            added += 1
        else:
            result = await db.execute(select(Concept.id).where(Concept.slug == concept_data["slug"]))
            slug_to_id[concept_data["slug"]] = result.scalar_one()

    existing_edges = await db.execute(select(ConceptPrerequisite.concept_id, ConceptPrerequisite.prerequisite_id))
    existing_edge_set = set()
    for row in existing_edges.fetchall():
        existing_edge_set.add((row[0], row[1]))

    edge_count = 0
    for prereq_slug, concept_slug, is_required in PREREQUISITES_SEED:
        if prereq_slug in slug_to_id and concept_slug in slug_to_id:
            edge_pair = (slug_to_id[concept_slug], slug_to_id[prereq_slug])
            if edge_pair not in existing_edge_set:
                edge = ConceptPrerequisite(
                    concept_id=slug_to_id[concept_slug],
                    prerequisite_id=slug_to_id[prereq_slug],
                    is_required=is_required,
                )
                db.add(edge)
                edge_count += 1

    await db.commit()
    return {"status": "seeded", "concepts_added": added, "total_concepts": len(CONCEPTS_SEED), "edges_added": edge_count}
