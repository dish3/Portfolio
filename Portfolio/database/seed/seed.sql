-- ==============================================================================
-- NOVA AI Portfolio OS — Initial Connectors Seed
-- Pre-registers supported platform connectors with enabled=false.
-- NOTE: X / Twitter is permanently excluded from this system.
-- ==============================================================================

insert into connectors (platform, enabled, config) values
  ('github', false, '{"description": "GitHub Repository & Release Ingestion"}'::jsonb),
  ('leetcode', false, '{"description": "LeetCode Public Profile & Stats Poller"}'::jsonb),
  ('linkedin', false, '{"description": "LinkedIn Post URL/Text Manual Submission"}'::jsonb),
  ('kaggle', false, '{"description": "Kaggle Competitions & Notebooks (Future)"}'::jsonb),
  ('devpost', false, '{"description": "Devpost Hackathon Projects (Future)"}'::jsonb),
  ('hashnode', false, '{"description": "Hashnode Blog Articles (Future)"}'::jsonb),
  ('medium', false, '{"description": "Medium Technical Articles (Future)"}'::jsonb),
  ('codeforces', false, '{"description": "Codeforces Contest Ratings (Future)"}'::jsonb),
  ('hackerrank', false, '{"description": "HackerRank Badges & Skills (Future)"}'::jsonb),
  ('spotify', false, '{"description": "Spotify Currently Playing & Playlists (Future)"}'::jsonb),
  ('instagram', false, '{"description": "Photography Showcase (Future)"}'::jsonb)
on conflict (platform) do nothing;
