# Reporting Structure

These are the sections and their respective fields:

- Meta
    - **Candidate name, title and email**
    - **Engagement Information**
- Document Control
    - **Customer Contacts**
- Executive Summary
    - Executive Summary
    - Approach
    - **Scope**
    - **Assessment Overview and Recommendations**
- Network Penetration Testing Assessment Summary
    - Network Summary
    - Summary of Findings
- Internal Network Compromise Walkthrough
    - Walkthrough Summary
    - **Detailed Walkthrough**
- Remediation Summary
    - Remediation Summary
    - **Short Term**
    - **Medium Term**
    - **Long Term**
- Appendix
    - Finding Severities
    - **Host & Service Discovery**
    - **Subdomain Discovery**
    - **Exploited Hosts**
    - **Compromised Users**
    - **Changes/Host Cleanup**
    - **Flags Discovered**
    - **Domain Password Review**
- Findings
    - **Title**
    - **CWE**
    - **CVSS**
    - **Overview**
    - **Impact**
    - **Affected Components**
    - **Recommendations**
    - **References**
    - **Details**

Most fields already have default texts. These may be placeholders that you’ll need to fill in or stock text that’s pretty acceptable.

# Assessment Start

Fill these information when the assessment starts.

- Meta
    - **Candidate name, title and email**
    - **Engagement Information**
- Document Control
    - **Customer Contacts**
- Network Penetration Testing Assessment Summary
    - Network Summary
    - Summary of Findings
- Executive Summary
    - Executive Summary
    - Approach
    - **Scope**

## When A Host Or Service Is Discovered

Once you discover a live host and enumerate the available services (e.g., via an Nmap scan), you should fill in the appropriate appendix:

- Appendix
    - **Host & Service Discovery**

## When A Virtual Host Or Subdomain Is Discovered

You should fill in the appropriate appendix with both the domains provided in the scope of the engagement (if any) and those you discover during your penetration test:

- Appendix
    - **Subdomain Discovery**

## When A Security Finding Is Discovered

This is one of the most important and time-consuming triggers, so it’s crucial to handle it correctly.

For each security finding, you need to add a **Finding** to the report.

Fill out all the fields:

- Findings
    - **Title**
    - **CWE**
    - **CVSS**
    - **Overview**
    - **Impact**
    - **Affected Components**
    - **Recommendations**
    - **Details**
- Remediation Summary
    - **Short Term**
    - **Medium Term**
    - **Long Term**

## When You Get Foothold On A Host

Once you gain command execution on a host, it’s time to add it as exploited to the appropriate appendix.

You’ll also document the steps for this initial compromise in the compromise walkthrough.

- Internal Network Compromise Walkthrough
    - Walkthrough Summary
    - **Detailed Walkthrough**
- Appendix
    - **Exploited Hosts**

## When You Root A Host

Once you’ve gained the highest local privilege on a host (root or SYSTEM), fill out the following fields:

- Internal Network Compromise Walkthrough
    - **Detailed Walkthrough**
- Appendix
    - **Changes/Host Cleanup**

## When You Compromise A User

Once you gain control of a user, whether by obtaining their passwords, NTLM hash or however else, add this information to the appropriate appendix.

- Appendix
    - **Compromised Users**

## When You Capture A Flag

You captured a flag, great job! Now, add it to the appropriate appendix:

- Appendix
    - **Flags Discovered**

## When The Engagement Is Done

By the end of your engagement, if you followed the trigger methodology, your report should be over 90% complete. All that’s left is to finish the remaining fields and add some final polish.

The fields that need to be filled or revisited are:

- Executive Summary
    - **Assessment Overview and Recommendations**
- Remediation Summary
    - **Short Term**
    - **Medium Term**
    - **Long Term**
- Appendix
    - **Domain Password Review**