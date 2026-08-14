-- Paiz Builders — one-time Supabase setup
-- Run this once in the Supabase dashboard: SQL Editor → New query → paste → Run.
--
-- Security model:
--   * The public site uses the anon key and may ONLY insert new rows.
--   * Reading, updating, and deleting happen through the admin dashboard,
--     whose Node server uses the service_role key (bypasses RLS).

create table if not exists public.leads (
  id uuid primary key default gen_random_uuid(),
  received_at timestamptz not null default now(),
  status text not null default 'new',
  source text,
  name text,
  phone text,
  email text,
  project_type text,
  project_size text,
  property_type text,
  ownership text,
  timeline text,
  budget text,
  location text,
  zip text,
  area text,
  contact_pref text,
  notes text,
  message text,
  page text
);

create table if not exists public.calls (
  id uuid primary key default gen_random_uuid(),
  clicked_at timestamptz not null default now(),
  page text,
  label text
);

alter table public.leads enable row level security;
alter table public.calls enable row level security;

drop policy if exists "anon can insert leads" on public.leads;
create policy "anon can insert leads"
  on public.leads for insert to anon with check (true);

drop policy if exists "anon can insert calls" on public.calls;
create policy "anon can insert calls"
  on public.calls for insert to anon with check (true);
