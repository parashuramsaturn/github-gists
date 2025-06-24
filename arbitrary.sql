BEGIN;

-- Delete XPlan related tables
DELETE FROM xplan_xplancredentials;
DELETE FROM xplan_xplansyncprogress;
DELETE FROM xplan_xplanclientconflict;
DELETE FROM xplan_crmidentifier;

-- Delete Nudge table
DELETE FROM nudge;

-- Delete email followup emails first (they reference meeting_meetingnote)
DELETE FROM email_followupemail;

-- Delete meeting-related tables in order
DELETE FROM meeting_section;
DELETE FROM meeting_meetingnote;

-- Delete tasks (they reference client_account)
DELETE FROM task_task;

-- Delete client-related tables
DELETE FROM assignments_accountadvisorassignment;
DELETE FROM assignments_clientmanagerassignment;
DELETE FROM client_accountcontact;
DELETE FROM client_account;
DELETE FROM client_contact;

-- If everything looks good
COMMIT; 
