#!/usr/bin/env python3
"""
Example workflow demonstrating multi-agent system
Agents collaboratively create SIE study materials
"""

import sys
import json
from pathlib import Path
from agent_orchestrator import AgentOrchestrator, TaskStatus
from agent_interface import AgentVaultInterface


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def workflow_study_guide_creation():
    """
    Complete workflow: Create comprehensive study guide for options trading

    Flow:
    1. Research Agent: Gather information, create notes and flashcards
    2. Synthesis Agent: Create connections and summaries
    3. Review Agent: Verify accuracy and consistency
    """

    print_section("Multi-Agent Study Guide Creation Workflow")

    orchestrator = AgentOrchestrator()

    # ========== STEP 1: Research Agent ==========
    print_section("STEP 1: Research Agent - Content Creation")

    task_id_research = orchestrator.submit_task(
        task_type="content-creation",
        agent_id="claude-research",
        description="Research and create comprehensive study guide on options trading",
        input_data={
            "topic": "Options Trading",
            "subtopics": [
                "Call and Put Options",
                "Option Pricing",
                "Greeks (Delta, Gamma, Theta, Vega)",
                "Option Strategies"
            ],
            "depth": "comprehensive",
            "format": "structured-notes-with-flashcards"
        }
    )

    print(f"✓ Research task submitted: {task_id_research}")

    # Simulate research agent working
    research_agent = AgentVaultInterface("claude-research")

    # Create flashcards
    flashcards = [
        ("What is a call option?", "A contract giving the right to buy an asset at a specific price (strike price) by a certain date"),
        ("What is a put option?", "A contract giving the right to sell an asset at a specific price (strike price) by a certain date"),
        ("Define Delta", "Measures the rate of change of option price with respect to changes in the underlying asset price"),
        ("Define Theta", "Measures the rate of decay of an option's value as time to expiration decreases (time decay)"),
        ("Define Vega", "Measures the sensitivity of an option's price to changes in volatility of the underlying asset"),
        ("Bull Call Spread", "Long call at lower strike, short call at higher strike - bullish strategy with defined risk"),
        ("Iron Condor", "Sell OTM call spread and put spread - neutral strategy profiting from time decay"),
        ("What is implied volatility?", "The market's forecast of future volatility used to price options"),
    ]

    print(f"\nCreating {len(flashcards)} flashcards...")
    for front, back in flashcards:
        research_agent.create_flashcard(
            front=front,
            back=back,
            deck="options-trading",
            tags=["sie", "options", "derivatives"]
        )
    print(f"✓ Created {len(flashcards)} flashcards")

    # Write research notes
    research_notes = """# Options Trading - Comprehensive Study Guide

## 1. Introduction to Options

### What are Options?
Options are derivative contracts that give the holder the right (but not obligation) to buy or sell an underlying asset at a predetermined price on or before a specific date.

### Key Characteristics
- **Strike Price**: The predetermined price at which the option can be exercised
- **Expiration Date**: The last date the option can be exercised
- **Premium**: The price paid to purchase the option
- **Intrinsic Value**: The immediate profit if exercised (max(spot-strike, 0) for calls)
- **Time Value**: Remaining value in the option from time until expiration

## 2. Types of Options

### Call Options
- Right to buy the underlying asset
- Profits when asset price rises
- Max loss = premium paid
- Unlimited profit potential

### Put Options
- Right to sell the underlying asset
- Profits when asset price falls
- Max loss = premium paid
- Max profit = strike price - premium

## 3. The Greeks

### Delta (Δ)
- Rate of change of option price with underlying price
- Range: 0 to 1 (for calls), -1 to 0 (for puts)
- Approximately equals probability ITM at expiration

### Gamma (Γ)
- Rate of change of delta
- Highest for ATM options
- Increases as expiration approaches

### Theta (Θ)
- Time decay of option value
- Benefits short positions, hurts long positions
- Accelerates as expiration approaches
- Usually negative for long positions

### Vega (ν)
- Sensitivity to volatility changes
- Positive for both calls and puts
- Higher for ATM options

### Rho (ρ)
- Sensitivity to interest rate changes
- More important for longer-dated options

## 4. Option Pricing Models

### Black-Scholes Model
Primary model used for European options:
- Inputs: Stock price, strike price, time to expiration, volatility, risk-free rate
- Output: Theoretical option price
- Assumes: No dividends, European exercise, lognormal distribution

### Binomial Model
Used for American options:
- More flexible than Black-Scholes
- Can handle early exercise
- Recombining tree of price movements

## 5. Option Strategies

### Bullish Strategies
1. **Long Call**: Buy call - profit from rising prices
2. **Bull Call Spread**: Buy call, sell higher strike call - reduced cost
3. **Bull Put Spread**: Sell lower strike put, buy higher strike put - credit spread

### Bearish Strategies
1. **Long Put**: Buy put - profit from falling prices
2. **Bear Call Spread**: Short lower strike call, long higher strike call
3. **Bear Put Spread**: Short higher strike put, long lower strike put

### Neutral Strategies
1. **Straddle**: Buy call and put at same strike - profit from volatility
2. **Strangle**: Buy OTM call and put - cheaper than straddle
3. **Iron Condor**: Sell call spread and put spread - profit from theta decay
4. **Butterfly**: Long 1 ITM, short 2 ATM, long 1 OTM - limited risk

### Volatility Strategies
1. **Calendar Spread**: Same strike, different expirations - profit from time decay
2. **Diagonal Spread**: Different strikes and expirations
3. **Ratio Spread**: Different number of contracts

## 6. Risk Management

### Assignment Risk
- Short option holders subject to assignment
- Increases as option goes ITM
- Certain for ITM options at expiration

### Early Exercise
- American options can be exercised anytime
- Early exercise usually on puts (for dividends/interest)
- Considered in pricing

### Position Greeks
- Calculate Greeks for entire portfolio
- Manage delta exposure (hedge if needed)
- Monitor gamma risk
- Plan for theta decay effects

## 7. Key Concepts for SIE Exam

- Understand calls vs puts
- Know the Greeks and what they measure
- Recognize basic strategies and their risk/reward
- Understand assignment and exercise
- Know Black-Scholes inputs and assumptions
"""

    research_agent.write_note(
        "Core-Ops/research-agent/options-trading-guide.md",
        research_notes,
        tags=["sie", "options", "comprehensive-guide"]
    )
    print("✓ Wrote comprehensive options trading guide")

    # Log activity
    research_agent.log_activity("research_complete", {
        "topic": "Options Trading",
        "flashcards_created": len(flashcards),
        "guide_written": True,
        "sections": 7
    })

    # Update task status
    orchestrator.update_task_status(
        task_id_research,
        TaskStatus.COMPLETED,
        result={
            "notes_created": 1,
            "flashcards_created": len(flashcards),
            "content_path": "Core-Ops/research-agent/options-trading-guide.md"
        }
    )
    print(f"✓ Research task completed: {task_id_research}")

    # ========== STEP 2: Synthesis Agent ==========
    print_section("STEP 2: Synthesis Agent - Create Connections")

    task_id_synthesis = orchestrator.submit_task(
        task_type="synthesis",
        agent_id="claude-synthesis",
        description="Synthesize options trading with other derivatives and market concepts",
        input_data={
            "source_content": "Core-Ops/research-agent/options-trading-guide.md",
            "connect_topics": ["Futures", "Stocks", "Risk Management", "Hedging"],
            "create_summary": True
        }
    )

    print(f"✓ Synthesis task submitted: {task_id_synthesis}")

    # Simulate synthesis agent working
    synthesis_agent = AgentVaultInterface("claude-synthesis")

    synthesis_content = """# Options in Context: Connections and Relationships

## Options vs Other Derivatives

### Options vs Futures
| Aspect | Options | Futures |
|--------|---------|---------|
| Obligation | Right, not obligation | Obligation to buy/sell |
| Premium | Paid upfront | No premium, margin required |
| Profit potential | Limited (calls) / Unlimited | Unlimited both directions |
| Risk | Limited to premium | Potentially unlimited |
| Exercise | At holder's discretion | Automatic at expiration |

### Options vs Stocks
- **Leverage**: Options provide leverage with limited capital
- **Directional**: Both can profit from price moves
- **Time decay**: Options lose value, stocks don't
- **Dividend impact**: Affect option prices, always affect stock prices

## Options Role in Portfolio Management

### Hedging Applications
- **Portfolio Insurance**: Long puts protect against downside
- **Cost Reduction**: Sell calls to fund puts (collars)
- **Income Generation**: Covered calls, cash-secured puts

### Risk Management Strategies
- Delta hedging for market-neutral positions
- Gamma management to control rehedging needs
- Theta harvesting in neutral markets

## Integration with SIE Curriculum

Options are tested in context of:
1. Product knowledge (types and mechanics)
2. Risk management (Greeks and hedge ratios)
3. Regulatory issues (margin requirements, assignment risk)
4. Client suitability (risk tolerance matching)
5. Market structures (volatility, exercise features)

## Key Relationships to Remember

- **Volatility ↑** → Call/Put premiums ↑
- **Intrinsic Value** = underlying advantage to exercise
- **Time Value** = premium - intrinsic value
- **In-The-Money (ITM)** = intrinsic value present
- **Out-of-The-Money (OTM)** = all premium is time value
"""

    synthesis_agent.write_note(
        "Core-Ops/synthesis-agent/options-context-and-connections.md",
        synthesis_content,
        tags=["sie", "options", "synthesis", "relationships"]
    )
    print("✓ Created cross-topic connections and summary")

    # Send message to research agent
    synthesis_agent.send_message_to_agent("claude-research", {
        "type": "synthesis_complete",
        "message": "Synthesis of options content complete, ready for review",
        "content_path": "Core-Ops/synthesis-agent/options-context-and-connections.md"
    })
    print("✓ Notified research agent of synthesis completion")

    synthesis_agent.log_activity("synthesis_complete", {
        "source_topic": "Options Trading",
        "connections_created": 3,
        "summary_written": True
    })

    orchestrator.update_task_status(
        task_id_synthesis,
        TaskStatus.COMPLETED,
        result={
            "connections_created": 3,
            "summary_created": True,
            "content_path": "Core-Ops/synthesis-agent/options-context-and-connections.md"
        }
    )
    print(f"✓ Synthesis task completed: {task_id_synthesis}")

    # ========== STEP 3: Review Agent ==========
    print_section("STEP 3: Review Agent - Quality Assurance")

    task_id_review = orchestrator.submit_task(
        task_type="content-review",
        agent_id="claude-review",
        description="Review all options content for accuracy and consistency",
        input_data={
            "content_paths": [
                "Core-Ops/research-agent/options-trading-guide.md",
                "Core-Ops/synthesis-agent/options-context-and-connections.md"
            ],
            "focus_areas": ["accuracy", "consistency", "completeness", "clarity"],
            "exam_context": "SIE"
        }
    )

    print(f"✓ Review task submitted: {task_id_review}")

    # Simulate review agent working
    review_agent = AgentVaultInterface("claude-review")

    review_feedback = """# Options Content Review - Quality Assessment

## Review Summary
- **Overall Quality**: Excellent
- **Accuracy**: High - all definitions and concepts verified
- **Consistency**: Good - terminology used consistently
- **Completeness**: Comprehensive for SIE exam
- **Clarity**: Clear explanations with good examples

## Strengths
1. ✓ Excellent coverage of basic option concepts
2. ✓ Greeks explained with practical implications
3. ✓ Good variety of strategy examples
4. ✓ Clear connections to broader market concepts
5. ✓ Well-organized for study purposes

## Recommendations
1. Consider adding more worked examples for option pricing
2. Include more real-world scenario applications
3. Add regulatory considerations for FINRA rules
4. Consider visual aids for strategy payoff diagrams

## Flashcard Quality
- All 8 flashcards are appropriate and helpful
- Questions are clear, answers are concise
- Good progression from basic to advanced

## Exam Readiness
Content adequately covers SIE exam topics for:
- Option mechanics and terminology
- Basic option strategies
- Risk management with options
- Option Greeks and their applications

## Approved for Inclusion
This content meets quality standards for inclusion in study materials.
"""

    review_agent.write_note(
        "Core-Ops/review-agent/options-content-review.md",
        review_feedback,
        tags=["sie", "options", "review", "quality-assurance"]
    )
    print("✓ Generated quality review and feedback")

    # Send approval message
    review_agent.send_message_to_agent("claude-research", {
        "type": "review_complete",
        "status": "approved",
        "message": "All options content approved for inclusion in study materials",
        "review_path": "Core-Ops/review-agent/options-content-review.md"
    })
    print("✓ Sent approval notification to research agent")

    review_agent.log_activity("review_complete", {
        "content_reviewed": 2,
        "status": "approved",
        "recommendations": 4
    })

    orchestrator.update_task_status(
        task_id_review,
        TaskStatus.COMPLETED,
        result={
            "files_reviewed": 2,
            "status": "approved",
            "recommendations": 4,
            "review_path": "Core-Ops/review-agent/options-content-review.md"
        }
    )
    print(f"✓ Review task completed: {task_id_review}")

    # ========== SUMMARY ==========
    print_section("WORKFLOW COMPLETE - SUMMARY")

    print("Created study materials:")
    print("  1. Comprehensive options trading guide (8 sections)")
    print("  2. 8 flashcards covering key concepts")
    print("  3. Cross-topic connections and relationships")
    print("  4. Quality review with recommendations")

    print("\nTask timeline:")
    print(f"  • Research: {task_id_research} → COMPLETED")
    print(f"  • Synthesis: {task_id_synthesis} → COMPLETED")
    print(f"  • Review: {task_id_review} → COMPLETED")

    print("\nFiles created:")
    print("  • Core-Ops/research-agent/options-trading-guide.md")
    print("  • Core-Ops/synthesis-agent/options-context-and-connections.md")
    print("  • Core-Ops/review-agent/options-content-review.md")
    print("  • Flashcards/options-trading/card_*.md (8 cards)")

    print("\nActivity logs:")
    print("  • Multi-Agent-System/logs/claude-research.jsonl")
    print("  • Multi-Agent-System/logs/claude-synthesis.jsonl")
    print("  • Multi-Agent-System/logs/claude-review.jsonl")

    print("\nAll tasks and logs saved to Multi-Agent-System/")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    try:
        workflow_study_guide_creation()
        print("✓ Workflow completed successfully!\n")
    except Exception as e:
        print(f"✗ Workflow error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
