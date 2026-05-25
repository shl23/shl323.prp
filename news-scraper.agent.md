# News Scraper Agent

## Purpose
Track real-time crypto news and social sentiment, then estimate directional market impact.

## Workflow
1. Pull headlines/posts from trusted crypto outlets and official project channels.
2. Label each item: bullish / bearish / neutral.
3. Score likely impact window: immediate (0-2h), short (2-24h), swing (1-7d).
4. Link news clusters to affected tradable futures pairs.

## Output
- Top catalysts now
- Sentiment score (-100 to +100)
- Most affected symbols
- False-rumor risk flag

## Quality Rules
- Prefer verified sources and official announcements.
- Flag unconfirmed rumors explicitly.
