import sys
import os
from datetime import datetime
from data.universities import UNIVERSITIES, SCHOLARSHIPS_DB


def get_ai_response(messages, user_message):
    query = user_message.strip().lower()

    # Help guide / default greeting
    greetings = ["hi", "hello", "assalam", "hey", "aoa", "salaam", "greetings"]
    if any(g in query for g in greetings) or query in ["help", "menu", "what can you do"]:
        return """👋 **Assalam-o-Alaikum!** I am the **AdmitWise Rule-Based Advisor**. I am here to guide you through university admissions in Pakistan. 

You can ask me about:
- 🏫 **Specific Universities**: Type a university name (e.g., *'NUST'*, *'FAST'*, *'LUMS'*, *'GIKI'*, *'PU'*)
- 💸 **Fees & Costs**: Type *'fees'*, *'affordable'*, or *'fee per year'*
- 💰 **Scholarships**: Type *'scholarships'* or specific ones like *'PEEF'* or *'Ehsaas'*
- 🗓️ **Deadlines**: Type *'deadlines'* to see upcoming application dates
- 🎯 **Merit Formulas**: Type *'merit formula'* or *'entry test'*
- ⚖️ **Comparison**: Type *'compare NUST and FAST'* or *'LUMS vs NUST'*
- 📍 **Cities**: Type a city name (e.g., *'Karachi'*, *'Lahore'*, *'Islamabad'*)

How can I assist you in your academic journey today?"""

    # Deadlines query
    if any(k in query for k in ["deadline", "date", "apply"]):
        deadline_text = "🗓️ **Upcoming University Admission Deadlines (2026):**\n\n"
        sorted_unis = sorted(UNIVERSITIES, key=lambda x: x["deadline"])
        for u in sorted_unis:
            try:
                days = (datetime.strptime(u["deadline"], "%Y-%m-%d") - datetime.now()).days
                if days < 0:
                    status = "❌ Closed"
                elif days <= 7:
                    status = f"🔴 Closing soon! ({days} days left)"
                else:
                    status = f"✅ Open ({days} days left)"
            except Exception:
                status = f"📅 Deadline: {u['deadline']}"
            deadline_text += f"- **{u['name']}** ({u['city']}): {u['deadline']} — {status}\n"
        return deadline_text

    # Scholarships query
    if any(k in query for k in ["scholarship", "financial aid", "peef", "ehsaas", "hec need", "laptop"]):
        # Check if user named a specific scholarship
        specific_sch = None
        for sch in SCHOLARSHIPS_DB:
            if sch["name"].lower() in query or sch["provider"].lower() in query:
                specific_sch = sch
                break

        if specific_sch:
            return f"""🎓 **Scholarship Profile: {specific_sch['name']}**
- **Provider**: {specific_sch['provider']}
- **Award Type**: {specific_sch['type']}
- **Amount/Coverage**: {specific_sch['amount']}
- **Eligibility Criteria**: {specific_sch['eligibility']}
- **Deadline**: {specific_sch['deadline']}
- 🌐 **[Official Link]({specific_sch['link']})**"""

        sch_text = "🎓 **Available Scholarships in Pakistan:**\n\n"
        for s in SCHOLARSHIPS_DB:
            sch_text += f"- **{s['name']}** ({s['provider']})\n"
            sch_text += f"  - **Coverage**: {s['amount']}\n"
            sch_text += f"  - **Eligibility**: {s['eligibility']}\n"
            sch_text += f"  - **Application Link**: [Click here]({s['link']})\n\n"
        return sch_text

    # Fees query
    if any(k in query for k in ["fee", "fees", "cost", "expensive", "cheap", "affordable", "price"]):
        # Check if user mentioned a specific university
        matching_uni = None
        for u in UNIVERSITIES:
            if u["name"].lower() in query or u["full_name"].lower() in query:
                matching_uni = u
                break

        if matching_uni:
            return f"💰 **{matching_uni['name']} Fee Structure:**\n- **Annual Tuition Fee**: PKR {matching_uni['fee_per_year']:,}\n- **Website**: {matching_uni['website']}"

        fee_text = "💸 **AdmitWise University Fee Overview (Per Year):**\n\n"
        fee_text += "🏫 **Public Sector Universities (Affordable):**\n"
        public_unis = [u for u in UNIVERSITIES if u["fee_per_year"] <= 80000]
        public_unis.sort(key=lambda x: x["fee_per_year"])
        for u in public_unis:
            fee_text += f"- **{u['name']}** ({u['city']}): PKR {u['fee_per_year']:,} / year\n"

        fee_text += "\n🏫 **Private & Premium Universities:**\n"
        private_unis = [u for u in UNIVERSITIES if u["fee_per_year"] > 80000]
        private_unis.sort(key=lambda x: x["fee_per_year"])
        for u in private_unis:
            fee_text += f"- **{u['name']}** ({u['city']}): PKR {u['fee_per_year']:,} / year\n"
        return fee_text

    # Comparison query (e.g. LUMS vs NUST)
    if "vs" in query or "compare" in query:
        found_unis = []
        for u in UNIVERSITIES:
            if u["name"].lower() in query:
                found_unis.append(u)

        # Deduplicate
        seen = set()
        found_unis = [u for u in found_unis if not (u["id"] in seen or seen.add(u["id"]))]

        if len(found_unis) >= 2:
            u1, u2 = found_unis[0], found_unis[1]
            return f"""⚖️ **Comparison: {u1['name']} vs {u2['name']}**

| Feature | {u1['name']} | {u2['name']} |
| :--- | :--- | :--- |
| **Full Name** | {u1['full_name']} | {u2['full_name']} |
| **City** | {u1['city']} | {u2['city']} |
| **National Ranking** | #{u1['ranking']} | #{u2['ranking']} |
| **Annual Fee** | PKR {u1['fee_per_year']:,} | PKR {u2['fee_per_year']:,} |
| **Entry Test** | {u1['entry_test']} | {u2['entry_test']} |
| **Min FSC Requirement** | {u1['min_fsc_percent']}% | {u2['min_fsc_percent']}% |
| **Admissions Deadline** | {u1['deadline']} | {u2['deadline']} |
| **Website** | [Visit Website]({u1['website']}) | [Visit Website]({u2['website']}) |

Both universities are excellent choices! {u1['name']} is famous for {", ".join(u1['fields'][:2])} while {u2['name']} is well-regarded for {", ".join(u2['fields'][:2])}."""
        else:
            return "⚖️ **Compare Universities**: Please mention at least two universities in your query (for example, type *'compare NUST and FAST'* or *'LUMS vs GIKI'*)."

    # Fields query (e.g., computer science, CS, engineering, medical)
    field_keywords = {
        "computer science": ["computer science", "cs", "software", "artificial intelligence", "ai", "cyber", "data science"],
        "engineering": ["engineering", "electrical", "civil", "mechanical", "chemical"],
        "medical": ["medical", "mbbs", "bds", "pharmacy", "nursing", "doctor"],
        "business": ["business", "bba", "finance", "accounting", "management", "marketing"],
        "law": ["law", "llb"],
        "mathematics": ["mathematics", "math", "statistics", "stats"],
        "social sciences": ["social sciences", "economics", "psychology", "sociology", "political science"]
    }

    matched_field = None
    for field_name, keywords in field_keywords.items():
        if any(k in query for k in keywords):
            matched_field = field_name
            break

    if matched_field:
        title = matched_field.title()
        field_unis = [u for u in UNIVERSITIES if any(f.lower() == matched_field for f in u["fields"])]

        reply = f"📖 **Universities offering {title} programs in Pakistan:**\n\n"
        for u in field_unis:
            sub = u["subfields"].get(title, u["subfields"].get(title.lower(), []))
            subfields_str = ", ".join(sub) if sub else "General programs"

            formula_info = ""
            criteria = u["merit_criteria"].get(title, u["merit_criteria"].get(title.lower(), None))
            if criteria:
                weights = []
                if criteria.get("matric_weight"): weights.append(f"{criteria['matric_weight']}% Matric")
                if criteria.get("fsc_weight"): weights.append(f"{criteria['fsc_weight']}% FSc")
                if criteria.get("net_weight"): weights.append(f"{criteria['net_weight']}% Test")
                formula_info = f" (Formula: {' + '.join(weights)})"

            reply += f"- **{u['name']}** ({u['city']}):\n"
            reply += f"  - **Specializations**: {subfields_str}\n"
            reply += f"  - **Entry Test**: {u['entry_test']}{formula_info}\n"
            reply += f"  - **Fee**: PKR {u['fee_per_year']:,} / year\n\n"
        return reply

    # Cities query (e.g. Lahore, Karachi, Islamabad)
    for city in ["lahore", "karachi", "islamabad", "peshawar", "topi", "rawalpindi"]:
        if city in query:
            city_unis = [u for u in UNIVERSITIES if u["city"].lower() == city]
            if city_unis:
                reply = f"📍 **Universities in {city.capitalize()}:**\n\n"
                for u in sorted(city_unis, key=lambda x: x["ranking"]):
                    reply += f"- **{u['name']}** — *{u['full_name']}*\n"
                    reply += f"  - **Ranking**: #{u['ranking']} | **Fee**: PKR {u['fee_per_year']:,} / year\n"
                    reply += f"  - **Key Fields**: {', '.join(u['fields'])}\n"
                    reply += f"  - **Deadline**: {u['deadline']}\n\n"
                return reply

    # Specific University Info check
    matched_uni = None
    for u in UNIVERSITIES:
        if u["name"].lower() in query or u["full_name"].lower() in query:
            matched_uni = u
            break

    if matched_uni:
        fields_str = ", ".join(matched_uni["fields"])
        scholarships_str = ", ".join(matched_uni["scholarships"]) if matched_uni["scholarships"] else "No specific scholarships listed"
        facilities_str = ", ".join(matched_uni["facilities"])

        return f"""🏫 **University Profile: {matched_uni['name']} ({matched_uni['full_name']})**
- **Location**: {matched_uni['city']}, {matched_uni['province']}
- **AdmitWise Ranking**: #{matched_uni['ranking']}
- **About**: {matched_uni['description']}
- **Admission Deadline**: {matched_uni['deadline']}
- **Annual Fee**: PKR {matched_uni['fee_per_year']:,}
- **Entry Test**: {matched_uni['entry_test']}
- **Min FSC Grade**: {matched_uni['min_fsc_percent']}%
- **Offered Fields**: {fields_str}
- **Available Scholarships**: {scholarships_str}
- **Facilities**: {facilities_str}
- 📧 **Admissions Contact**: {matched_uni['contact']}
- 🌐 **[Official Website]({matched_uni['website']})**"""

    # Merit Formulas general query
    if any(k in query for k in ["merit", "formula", "entry test", "ecat", "net", "nat", "mdcat"]):
        merit_text = "🎯 **Common University Merit Calculations:**\n\n"
        for u in UNIVERSITIES[:6]:
            merit_text += f"- **{u['name']}** ({u['entry_test']}):\n"
            first_field = u["fields"][0]
            criteria = u["merit_criteria"].get(first_field, None)
            if criteria:
                weights = []
                if criteria.get("matric_weight"): weights.append(f"{criteria['matric_weight']}% Matric")
                if criteria.get("fsc_weight"): weights.append(f"{criteria['fsc_weight']}% FSc")
                if criteria.get("net_weight"): weights.append(f"{criteria['net_weight']}% Entry Test")
                merit_text += f"  - **Merit Formula**: {' + '.join(weights)}\n"
            merit_text += f"  - **Min FSC**: {u['min_fsc_percent']}%\n\n"
        return merit_text

    # Default fallback
    return f"""🤖 I could not find an exact match for your question: *"{user_message}"*. 

As a rule-based advisor, I work best with specific topics. Please try asking about:
- **Specific university** (e.g. *'Tell me about NUST'*, *'FAST'*, *'LUMS'*)
- **Fees** (e.g. *'Which universities have lowest fees?'*, *'FAST fees'*)
- **Scholarships** (e.g. *'What scholarships are available?'*, *'HEC scholarship'*)
- **Deadlines** (e.g. *'admissions deadlines'*)
- **Cities** (e.g. *'universities in Lahore'*, *'universities in Karachi'*)
- **Fields of Study** (e.g. *'Which universities offer computer science?'*)
- **Comparisons** (e.g. *'compare NUST and FAST'*)

Type **'help'** to see the main guide."""
