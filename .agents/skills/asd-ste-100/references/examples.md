# ASD-STE-100 Examples

Each example shows a problem, the rule that it breaks, and the rewrite.

## Passive voice in a procedure (rule 3.5)

**Before:** The configuration file must be edited before the service is
restarted.

**After:** Edit the configuration file. Then start the service again.

## Nominalization (rule 3.6)

**Before:** Perform a verification of the checksum before the installation of
the package.

**After:** Check the checksum. Then install the package.

## Long sentence with many topics (rules 4.5, 5.6)

**Before:** If the deployment fails because the image cannot be pulled from the
registry, which usually happens when the credentials have expired, you should
refresh the token and then retry the deployment from the pipeline.

**After:**

> A deployment fails if the system cannot get the image from the registry.
> Usually, the cause is an expired credential. To correct the problem, do these
> steps:
>
> 1. Refresh the token.
> 2. Start the deployment again from the pipeline.

## Noun cluster (rule 2.1)

**Before:** Increase the container runtime memory limit configuration value.

**After:** Increase the value of the memory limit in the configuration of the
container runtime.

## More than one instruction in one sentence (rule 5.2)

**Before:** Stop the server, back up the database, and apply the migration.

**After:**

1. Stop the server.
2. Make a backup of the database.
3. Apply the migration.

## Deleted articles (rule 4.3)

**Before:** Set flag in config file to enable feature.

**After:** Set the flag in the configuration file to enable the feature.

## Not-approved words (rules 1.1, 1.11)

**Before:** Utilize the CLI to facilitate the initialization of the workspace.

**After:** Use the command-line interface to start the workspace.

## Complex tense (rule 3.3)

**Before:** The agent has been retrying the request for five minutes.

**After:** The agent started the request five minutes ago. It tries again each
30 seconds.

## Safety instruction after the step (rule 7.1)

**Before:**

> Run `terraform apply`. Warning: this command deletes the production database.

**After:**

> **Warning:** The `terraform apply` command deletes the production database.
> Make sure that you have a backup.
>
> Run `terraform apply`.

## Word with the wrong meaning (rule 1.3)

**Before:** Follow the steps in the security policy.

**After:** Obey the steps in the security policy.

## Vague quantity (rule 4.2)

**Before:** The cache is cleared periodically.

**After:** The system clears the cache each 15 minutes.

## Note that contains an instruction (rule 9.2)

**Before:** Note: You must set the `TOKEN` variable first.

**After:** Set the `TOKEN` variable first.

## Slash for "and" or "or" (rule 8.3)

**Before:** Use the start/stop buttons.

**After:** Use the start button or the stop button.

## Parenthesis that adds information (rule 8.4)

**Before:** The build cache (which the runner keeps for seven days) makes the
build faster.

**After:** The build cache makes the build faster. The runner keeps the cache
for seven days.

## A complete rewrite

**Before:**

> In order to facilitate troubleshooting of intermittent connectivity issues,
> comprehensive diagnostic logging capabilities have been implemented, which
> can be enabled by modification of the verbosity parameter, although it should
> be noted that this will result in significantly increased disk utilization.

**After:**

> The system can write diagnostic logs. The logs help you to find the cause of
> a connection problem that occurs sometimes.
>
> To write the diagnostic logs, change the verbosity parameter.
>
> **Caution:** Diagnostic logs use much disk space. Make sure that the disk has
> enough free space.
