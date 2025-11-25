# TalentPilot System Prompt Implementation

## Overview
The complete TalentPilot system prompt has been implemented across your HR agent application. The agent now follows the comprehensive Elite HR Orchestration Agent architecture in every chat interaction.
'
## Files Modified/Created

### 1. **Created: `lib/talentPilotSystemPrompt.js`**
- **Purpose**: Centralized system prompt management
- **Contains**: Complete TalentPilot Elite HR Orchestration Agent system architecture
- **Exports**: `TALENTPILOT_SYSTEM_PROMPT` constant
- **Features**:
  - Three-Tier Knowledge System (Tier 1: Internal Compliance, Tier 2: Autonomous Reasoning, Tier 3: External Intelligence)
  - Decision Matrix Protocol for intelligent source selection
  - Advanced reasoning protocols
  - Behavioral excellence standards
  - Safety, ethics & compliance guardrails
  - Performance standards and quality checklist

### 2. **Modified: `lib/openrouter.js`**
- **Change**: Imports and uses the centralized system prompt
- **Before**: Inline short system prompt (~50 lines)
- **After**: Uses comprehensive `TALENTPILOT_SYSTEM_PROMPT` from external module
- **Benefit**: Centralized prompt management, easier updates, clean separation of concerns

## System Prompt Architecture

### Three-Tier Knowledge System

**TIER 1: INTERNAL COMPLIANCE (Highest Authority)**
- Company policies, documents, procedures
- Exact numbers (PTO days, budgets, headcount)
- Internal templates and forms
- Company-specific programs (benefits, perks, training)
- Mandatory knowledge base check before responding

**TIER 2: AUTONOMOUS REASONING (Your Intelligence)**
- General HR best practices
- Creative tasks (drafting, writing, creating)
- Coaching and strategic guidance
- Interview question generation
- Performance management frameworks
- Leadership techniques
- D.E.I. best practices

**TIER 3: EXTERNAL INTELLIGENCE (Real-Time Web)**
- Time-sensitive information
- Market salary and compensation data
- Industry trends and benchmarks
- Regulatory changes
- Technology recommendations
- Current hiring market conditions

### Decision Matrix Protocol

The agent classifies every query:

1. **Query Classification**
   - Company-Specific Factual Query
   - General HR Best Practice Query
   - Creative/Drafting Task
   - Market/External Data Query
   - Complex Multi-Step Problem

2. **Source Routing**
   - Routes to appropriate knowledge tier
   - Executes decision rigorously
   - Cites sources with authority

### Advanced Reasoning Protocols

1. **Step-by-Step Problem Decomposition** - Make thinking visible
2. **Proactive Value Addition** - Answer beyond the literal question
3. **Intelligent Clarification** - Ask targeted questions when context missing
4. **Confidence Calibration** - Be honest about certainty levels

## Behavioral Standards Implemented

### Communication Excellence
- Tone calibration by context (urgent, routine, complex, teaching)
- Clear, action-oriented writing
- Structure with headers and bullets
- Professional representation of organization

### Proactive Assistance
- Anticipate related needs
- Offer next steps without being asked
- Provide templates and frameworks
- Enable continuous support

### Error Recovery
- Acknowledge mistakes immediately
- Correct with proper source citation
- Transparent about limitations
- Never guess on important facts

## Safety & Compliance

### Non-Negotiables
- ❌ No discriminatory actions (protected characteristics)
- ❌ No privacy violations
- ❌ No legal/compliance risks
- ✅ Red flag detection and escalation to human HR

### Ethical Guardrails
- Transparency about knowledge sources
- Fairness in recommendations
- Privacy-first approach
- Compliance above all

## Quality Checklist

Every response verifies:
- ✅ Correct knowledge source used
- ✅ Sources cited for factual claims
- ✅ Actionable next steps provided
- ✅ Related needs anticipated
- ✅ Language clear and professional
- ✅ Strategic value added
- ✅ Legal/ethical concerns addressed
- ✅ Continued support offered

## Performance Standards

### Success Metrics
1. **Accuracy Rate**: 100% for internal policy, 95%+ for external data
2. **Response Completeness**: No follow-up needed for missing basics
3. **Source Appropriateness**: Correct tier used every time
4. **Value Addition**: Strategic insight beyond literal question
5. **User Satisfaction**: Users feel empowered

## How It Works in Practice

### Example Flow

**User**: "How many PTO days do I get?"

1. **Agent Classification**: Company-Specific Factual Query
2. **Source Routing**: TIER 1 - Internal Compliance
3. **Action**: Check company policy documents
4. **Response**: 
   - "According to our Leave Policy, full-time employees receive 15 PTO days per year, accrued monthly."
   - Cite exact source
   - Provide context (accrual schedule, part-time rates)
   - Proactive: "I can also help with PTO request processes or carryover policies"

**User**: "How should I conduct a performance review?"

1. **Agent Classification**: General HR Best Practice Query
2. **Source Routing**: TIER 2 - Autonomous Reasoning
3. **Action**: Apply HR best practices and frameworks
4. **Response**:
   - Provide structured approach
   - Include conversation framework
   - Add evaluation criteria
   - Offer related support (documentation templates, manager training)
   - Transparency: "This is based on HR best practices"

**User**: "What's the market salary for a Senior PM in Austin?"

1. **Agent Classification**: Market/External Data Query
2. **Source Routing**: TIER 3 - External Intelligence
3. **Action**: Search current market data
4. **Response**:
   - Provide salary range with sources
   - Synthesize multiple data sources
   - Contextualize variations
   - Include total compensation structure
   - Note recent data (date-stamped)

## Integration Points

### In `openrouter.js`
- System prompt injected into every API call to OpenRouter
- Applied to all model responses automatically
- Temperature: 0.7 (balanced creativity/consistency)
- Max tokens: 2048 (comprehensive responses)

### In Chat Interface (`app/chat/page.jsx`)
- All user messages processed with system prompt
- Agent behavior consistent across all interactions
- Greeting message reflects TalentPilot identity

## Maintenance & Updates

### To Update System Prompt
1. Edit `lib/talentPilotSystemPrompt.js`
2. Changes apply immediately to all new chats
3. No changes needed to other files
4. Version control tracks prompt evolution

### To Add New Capabilities
1. Update relevant section in `talentPilotSystemPrompt.js`
2. Ensure aligned with three-tier architecture
3. Add to corresponding behavioral standard
4. Test in chat to verify behavior

## Key Features Now Enabled

✅ Three-tier knowledge hierarchy with clear prioritization
✅ Decision matrix for intelligent source selection
✅ Advanced reasoning with visible thinking
✅ Proactive value addition
✅ Comprehensive ethical guardrails
✅ Red flag detection for escalation
✅ Quality checklist before every response
✅ Performance standards and metrics
✅ Error recovery and transparency
✅ Continuous improvement protocols

## Next Steps (Optional)

1. **Knowledge Base Integration**: Connect to actual company documents (HR policies, handbooks)
2. **CSV Data Connection**: Integrate recruitment_data.csv, employee_data.csv, etc.
3. **Multi-turn Conversation**: Add context retention across sessions
4. **User Role Detection**: Tailor responses based on employee/manager/HR user type
5. **Audit Logging**: Track prompts and responses for compliance

---

**Implementation Date**: November 23, 2025
**System Prompt Version**: 1.0 - Elite HR Orchestration Agent
**Status**: Active in all new chats
