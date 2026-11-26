---
id: TRN-RES-01
title: Competitive Research — Data Integration Platforms
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
accessed: 2026-11-26
source_register: docs/research/source-register.md
note: "Prepared by a research subagent from public web sources; prices marked Unverified were not confirmed on a vendor page. Vendor-authored complaint sources are labelled vendor-interested."
---

# Competitive Analysis: Data Integration and ELT Tools (as context for an embeddable F# integration engine)

- **Prepared:** 2026-11-26
- **Access date for every source below:** 2026-11-26 unless noted otherwise
- **Citation format:** `[SRC-nnn]` refers to the numbered source list at the end of the document.
- **Price-verification rule:** a price is marked **verified** only when it was read on the vendor's own page, or from the vendor's machine-readable price API in the case of Azure. Every other price is marked **unverified**.
- **Evidence caveat:** many complaint sources are competitor blogs, for example Hevo, Integrate.io, Estuary, Tobiko and Meltano writing about rivals. Those are flagged as *vendor-interested* where used. Review-site figures (G2, PeerSpot, Capterra) are snapshots and change over time.

---

## 0. Executive summary

1. **The market has consolidated sharply in 2025–2026.**
   - Salesforce closed its acquisition of Informatica on 18 Nov 2025 [SRC-017].
   - Fivetran acquired Tobiko Data, the company behind SQLMesh and SQLGlot, in Sep 2025 [SRC-077]. It then completed its merger with dbt Labs on 1 Jun 2026 [SRC-078].
   - Prefect announced the acquisition of Dagster Labs in July 2026. Dagster's FAQ said the deal was "expected to close in the coming weeks" [SRC-102][SRC-103][SRC-109].
   - Wikipedia reports, without a citation, that Pentaho was acquired by LEO Software (Constellation) in June 2026. Treat this as **unverified** [SRC-058].
   - Qlik retired Talend Open Studio on 31 Jan 2024 [SRC-043]. Pentaho moved away from a production-usable Community Edition with release 10.2 [SRC-057][SRC-058].
   - Net effect: **the open, embeddable, permissively licensed tier is shrinking.** That is an opening for a small embeddable engine.
2. **The modern stack has converged on four ideas:**
   - a *process-isolated connector protocol*: Singer and the Airbyte protocol, with JSON messages over stdin and stdout [SRC-063][SRC-110];
   - *transformations as versioned code with tests*: dbt and SQLMesh [SRC-080][SRC-121];
   - *asset- or data-centric orchestration*: Dagster [SRC-100];
   - *open lineage events*: OpenLineage [SRC-125].
3. **Legacy suites carry heavy historical baggage.** Examples:
   - GUI-authored artifacts serialized as designer-coupled XML, such as SSIS `.dtsx` and PDI `.ktr`/`.kjb` [SRC-030][SRC-032][SRC-061];
   - generated-Java runtimes, as in Talend [SRC-046];
   - mandatory server or agent runtimes and cluster spin-up, as in Glue, ADF data flows and Informatica Secure Agent [SRC-004][SRC-006][SRC-021].
4. **The most common cross-category complaints:**
   - unpredictable consumption pricing: Fivetran MAR, Informatica IPU, Glue DPU [SRC-002][SRC-075][SRC-092];
   - poor debuggability and opaque errors: ADF, Glue, dbt/Jinja [SRC-036][SRC-091][SRC-083];
   - connector fragility and upgrade churn: Airbyte [SRC-067][SRC-068];
   - steep learning curves: NiFi, PowerCenter, Dagster [SRC-054][SRC-023][SRC-104].
5. **AI-assisted configuration is now table stakes.** Every major vendor ships it:
   - Informatica CLAIRE GPT, agents and Copilot [SRC-018][SRC-019];
   - Fabric Data Factory Copilot [SRC-038];
   - Airbyte Connector Builder AI Assist [SRC-065];
   - Fivetran Connector SDK AI plugins for coding agents [SRC-072].

   These features generate artifacts in each vendor's own format. None produces a portable, testable spec, which is a design opening.

---

## 1. Product-by-product analysis

Each product is covered under the same headings: definition format, transformation language, connector model, staging, metadata and lineage, schema discovery and profiling, errors / checkpointing / incremental / CDC, testing, deployment and footprint, security, licensing and pricing, complaints, and AI features. Where a heading has no verified source, the entry says "not verified" rather than guessing.

### 1.1 Informatica PowerCenter and Intelligent Data Management Cloud (IDMC)

**Corporate status**
- Salesforce completed its acquisition of Informatica on 18 Nov 2025 and plans to fold Informatica's catalog, governance, quality, metadata and MDM into its platform [SRC-017].

**Lifecycle**
- PowerCenter 10.5.x reached end of standard support on 31 Mar 2026. Third-party guides report paid extended support to 31 Mar 2027 and sustaining support after that [SRC-011][SRC-012].
- Informatica steers customers to IDMC (Cloud Data Integration, CDI) with migration tooling. Services firms say complex mappings and custom logic often need manual remediation [SRC-012][SRC-013].

**Pipeline definition format**
- PowerCenter is GUI-designed: mappings, sessions and workflows live in a repository. IDMC CDI is also a visual, web-based mapping designer.

**Transformation language**
- A visual transformation graph plus Informatica's expression language.

**Connector model**
- Proprietary connectors run inside the runtime.
- In IDMC the runtime is the **Secure Agent**, described as "a lightweight program that runs all tasks". It is built from independently running services, for example the Data Integration Server [SRC-021].
- Secure Agent groups provide failover. Hosted Agents are Informatica-managed for cloud-to-cloud jobs [SRC-021].

**Staging**
- Runtime-side processing on the Secure Agent or Hosted Agent.
- Pushdown to the database or warehouse exists, but its specifics were not verified for this report.

**Metadata and lineage**
- Lineage lives in Cloud Data Governance and Catalog (CDGC).
- Lineage is produced by scanning catalog sources, rule-based or CLAIRE-generated linking, and "external lineage ingestion" [SRC-026].
- **No evidence found that CDGC consumes or emits OpenLineage.** A targeted search returned only other vendors, IBM and Google Knowledge Catalog, as OpenLineage consumers [SRC-026].

**Schema discovery and profiling**
- Not verified for this report. Profiling and data quality are separate IDMC services billed in IPUs [SRC-014].

**Errors, incremental loads and CDC**
- Not verified for this report. Mass Ingestion volume is one of the IPU metering "scalers" [SRC-014].

**Testing**
- No first-class tests-as-code support verified.

**Deployment and infrastructure footprint**
- PowerCenter: on-premises server, repository database and domain.
- IDMC: a SaaS control plane plus customer-hosted Secure Agents. Agents connect outbound over HTTPS/443 with TLS, so no inbound firewall ports are needed [SRC-021][SRC-022].

**Security notes**
- Data is processed by the Secure Agent in the customer environment. Only metadata and job status go to IDMC, per training material.
- The 2025 security whitepaper confirms that runtimes "connect, transform and move the data" within the customer's network or VPC [SRC-022].

**Licensing and pricing**
- IDMC sells prepaid capacity in **IPUs (Informatica Processing Units)**. A "Flex IPU" option and volume-tier discounts were added later [SRC-014][SRC-015].
- No per-IPU list price is published [SRC-015].
- A UK G-Cloud procurement listing reportedly shows a **£74,999 minimum** for Cloud Data Integration. **Unverified**, seen only in a search summary [SRC-016].
- Promotion: through 31 Jan 2027, eligible customers can use CLAIRE GPT, copilots and agents at no additional IPU cost. Job execution is excluded [SRC-020].

**Common complaints**
- Steep learning curve [SRC-023][SRC-025].
- Price "expensive and inflexible" [SRC-024].
- G2 places perceived cost at the top of its scale [SRC-023].
- Some reviewers call the UI dated. Others disagree [SRC-023].

**AI features**
- **CLAIRE GPT** uses a supervisor agent that coordinates Discovery, Data Exploration, Data Integration, Data Quality and Product Help agents [SRC-018].
- The Data Integration agent generates ELT and ETL mappings from natural language [SRC-018].
- **CLAIRE Copilot** for data integration reached GA in 2025. It generates, documents and optimizes pipelines [SRC-019].

### 1.2 Microsoft SQL Server Integration Services (SSIS)

**Pipeline definition format**
- Visual designer in Visual Studio. Packages are saved as **`.dtsx` XML**.
- Microsoft changed the format in SQL Server 2012 ("Denali") to make it "easier to read, and easier to diff" [SRC-030].
- Practitioners still report that lineage IDs and designer layout in the XML make merges break data flows. Moving a task on the canvas can change many lines of XML [SRC-032].
- The project file (`.dtproj`), connection managers and parameters are frequent sources of Git conflicts [SRC-031].

**Transformation language**
- Data-flow components plus the SSIS expression language, with C#/VB Script tasks and components.

**Connector model**
- Connection managers and data-flow sources and destinations, extended through .NET components and feature packs.
- SQL Server 2025 **removes** the Attunity CDC components and the CDC Service for Oracle, the Microsoft Connector for Oracle, and the Hadoop Hive, Pig and File System tasks [SRC-027][SRC-028][SRC-029].
- SQL Server 2025 deprecates the legacy Integration Services Service, 32-bit mode and the SDS connection type [SRC-027].

**Staging**
- In-memory data-flow buffers on the SSIS server. Not separately verified for this report.

**Metadata and lineage**
- No native OpenLineage support found.

**Errors and CDC**
- The CDC components were deprecated, with support ending 13 Dec 2025, and removed in 2025 [SRC-028].

**Testing**
- No first-class testing support verified.

**Deployment and infrastructure footprint**
- On-premises SQL Server licence, or the **Azure-SSIS Integration Runtime** in ADF.
- Azure-SSIS IR VM prices in East US, from the vendor's price API (**verified**) [SRC-006]:

  | VM | Standard, licence included | Enterprise, licence included | Azure Hybrid Benefit |
  |---|---|---|---|
  | D4 v3 | $0.969/h | $2.042/h | $0.579/h |

**Analyst view**
- Directions on Microsoft says SQL Server 2025 offers "little in the advancement of Integration Services", with a long list of removals [SRC-033].

**Complaints**
- Source control and merging (see above) [SRC-031][SRC-032].
- Platform stagnation [SRC-033].

**AI features**
- None verified for SSIS itself.

### 1.3 Azure Data Factory (ADF) and Fabric Data Factory

**Pipeline definition format**
- Visual authoring backed by **JSON resource definitions**.
- Git integration with Azure Repos or GitHub stores folders per resource type: pipeline, dataset, linked service, trigger and integration runtime [SRC-034].
- Deployment promotes an **ARM template** generated in a publish branch. Microsoft recommends enabling Git only on the development factory [SRC-034].
- Large factories hit ARM template limits and need linked templates [SRC-035].

**Transformation language**
- Pipeline expression language.
- Mapping Data Flows, which execute on managed Spark clusters billed per vCore-hour.
- Power Query, as "wrangling" data flows [SRC-006].

**Connector model**
- Linked services and datasets.
- Execution happens on an Integration Runtime: Azure, managed VNET, self-hosted or Azure-SSIS [SRC-005][SRC-006].

**Staging**
- The Copy activity can stage data.
- Data flows require a Spark cluster with a minimum of 8 vCores [SRC-005].

**Metadata and lineage**
- Purview integration exists, but was not verified for this report.
- No native OpenLineage emission verified.

**Errors, checkpointing and incremental loads**
- Activity-level retry and dependency conditions. Not separately verified for this report.

**Testing**
- No first-class unit testing verified.

**Deployment**
- PaaS.

**ADF pricing, East US, from the Azure Retail Prices API (verified, vendor source)** [SRC-006]. Meter names in brackets are the API's own.

| Meter | Azure IR | Self-hosted IR | Managed VNET IR |
|---|---|---|---|
| Orchestration, per 1,000 activity runs | $1.00 | $1.50 | $1.00 |
| Data movement, per DIU-hour (per hour for self-hosted) | $0.25 | $0.10 | $0.25 |
| Pipeline activity, per hour | $0.005 | $0.002 | $1.00 |
| External activity, per hour | $0.00025 | $0.0001 | $1.00 |
| Data Flow, General Purpose, per vCore-hour | $0.27325 | n/a | n/a |
| Data Flow, Memory Optimized, per vCore-hour | $0.34275 | n/a | n/a |
| Read/write operations, per 50,000 | $0.50 | $0.50 | n/a |
| Monitoring operations, per 50,000 | $0.25 | $0.25 | n/a |
| Inactive pipeline, per month | $0.80 | $0.80 | n/a |
| Managed Airflow (Small / Large), per hour | $0.49 / $0.99 | n/a | n/a |

The public ADF pricing page renders these values only in the browser through JavaScript, so the text-only fetch shows placeholders [SRC-005]. The API values above are the authoritative machine-readable source.

**Fabric Data Factory**
- Billed from Fabric capacity units (CU):
  - Copy activity: 1.5 CU-hours per "intelligent optimization throughput resource" hour.
  - Orchestration: 0.0056 CU-hours per activity run [SRC-040].
  - Copy job: 1.5 CU-hours for a full copy and 3 CU-hours for an incremental copy [SRC-041].
- Microsoft's worked example: a 1 TB Parquet load used 3,960 CU-seconds. At a **hypothetical** $0.18 per CU-hour, that came to about $0.20 [SRC-042]. The $0.18 rate is Microsoft's own illustration, not a verified list price for your region.

**Complaints**
- Debugging difficulty and vague or generic error messages are the most common G2 cons [SRC-036].
- Debug runs can fail with errors that differ from the monitoring pane [SRC-037].
- Cost is hard to estimate [SRC-036].

**AI features**
- **Copilot for Data Factory (Fabric)** generates pipelines from natural language, for example "copy data from Azure SQL to a Lakehouse and send a notification".
- It also summarizes and explains existing pipelines and generates or explains pipeline expressions [SRC-038][SRC-039].
- It requires Fabric capacity and tenant enablement. Sources disagree on whether it is preview or GA [SRC-038][SRC-039].

### 1.4 Talend (Qlik Talend Cloud / Talend Studio)

**Status**
- Qlik retired Talend Open Studio on 31 Jan 2024, citing "diminishing community adoption". It is no longer hosted or patched [SRC-043][SRC-049].
- A community fork, Talaxie, exists [SRC-049].

**Pipeline definition format**
- Eclipse-based visual Studio.
- **Studio is a code generator: each job is compiled to Java.** Oversized subjobs can hit the JVM 65,535-byte method-size limit and fail to compile [SRC-046].

**Transformation language**
- Visual components such as tMap, plus Java expressions [SRC-046].

**Connector model**
- Component palette. Generated code links connector libraries.

**Deployment and infrastructure footprint**
- Studio needs heap tuning. Qlik recommends raising Xmx, for example to 4096m, for big projects [SRC-047].
- Qlik Talend Cloud is SaaS with remote engines. Engine details were not verified for this report.

**Pricing**
- Capacity-based, not per seat [SRC-044]:
  - Starter and Standard are sized on **data moved**.
  - Premium and Enterprise also meter job runs, run time and lakehouse compute.
  - All editions include unlimited users.
- AWS Marketplace reportedly lists Starter at **$6,000 per 12 months for up to 50 GB per month**. **Unverified**, seen only in a search summary [SRC-045].

**Complaints**
- Studio consumes "large amount of memory" and takes minutes to open [SRC-048].
- GC-overhead failures on bulk data [SRC-048].
- Debugging often means reading generated Java. This comes from a vendor-interested source, summarized in [SRC-048].

**AI features**
- Not verified for this report.

### 1.5 Apache NiFi

**Pipeline definition format**
- Visual, browser-based flow canvas.
- Flows are versioned as **JSON flow definitions**. NiFi 2.x adds GitHub and GitLab Flow Registry Clients, so flows can be versioned directly in Git without a separate NiFi Registry [SRC-052][SRC-053].

**Transformation language**
- Processors written in Java, plus the NiFi Expression Language and record-oriented processors.
- **NiFi 2.0 added a native Python processor API** [SRC-051].

**Connector model**
- Processors and controller services, packaged as NARs.

**Staging and durability**
- Three on-disk repositories [SRC-050]:
  - **FlowFile repository:** a write-ahead log of FlowFile metadata.
  - **Content repository:** an "immutable versioned content store", copy-on-write.
  - **Provenance repository:** per-event snapshots that enable lineage and **replay**, with retention bounded by disk or age.

**Metadata and lineage**
- Built-in, fine-grained provenance per FlowFile [SRC-050].
- OpenLineage support not verified.

**Errors and checkpointing**
- Back-pressure and queueing on connections.
- Queues swap to disk above `nifi.queue.swap.threshold` [SRC-050].

**Testing**
- Java processor test harnesses exist. Not separately verified for this report.

**Deployment**
- JVM cluster.
- Stateless execution of process groups was introduced in 2.x [SRC-051].

**Licence**
- Apache 2.0, as an ASF project. There is no licence cost. Commercial distributions such as Cloudera carry their own pricing [SRC-054].

**Complaints**
- Steep learning curve [SRC-054].
- Memory- and CPU-hungry [SRC-055][SRC-056].
- Reported production crashes [SRC-054].
- Pain reading configuration metadata [SRC-054].

**AI features**
- None verified.

### 1.6 Pentaho Data Integration (PDI / Kettle)

**Pipeline definition format**
- **Transformations (`.ktr`) and jobs (`.kjb`) are XML files** authored in the **Spoon** GUI.
- They can be stored on the filesystem or in a repository, but the two cannot be mixed in one project [SRC-061].

**Runtime**
- **Pan** runs transformations, **Kitchen** runs jobs, and **Carte** is a remote execution web server [SRC-061].
- Transformations stream rows between steps.
- Product docs: [SRC-060].

**Connector model**
- Steps and plugins (Java).

**Licensing**
- With release 10.2, PDI moved to four licence tiers, including a new **Starter Edition**. A "PDI Starter pack" is offered to migrate Community Edition users [SRC-057].
- Wikipedia reports that the 10.2 Community Edition licence does not allow production use without a subscription, citing a Hitachi Vantara community post from 29 Aug 2024 [SRC-058].
- Hitachi's CE download page still lists 9.x builds [SRC-059].
- Ownership: reported acquisition by LEO Software in June 2026. **Unverified**: Wikipedia, uncited [SRC-058].

**Pricing**
- Not published. **Unverified.**

**Complaints**
- Reviewers report that the Community Edition is "almost not supported anymore" [SRC-062].

**AI features**
- None verified.

**Relevance**
- Apache Hop (section 1.12) is the community's modernised fork of the Kettle architecture [SRC-094].

### 1.7 Airbyte

**Pipeline definition format**
- UI, API or Terraform "connections" that pair a source with a destination plus a configured catalog. Terraform and API details were not verified for this report.

**Connector model: the Airbyte Protocol** [SRC-063]
- Actor commands:
  - `spec`: returns the connector specification;
  - `check`: validates the configuration and access;
  - `discover`: returns a catalog of streams (sources only);
  - `read`: takes config, configured catalog and state, and emits records and state;
  - `write`: reads messages from stdin and loads them (destinations only).
- Message types: `RECORD`, `STATE` (STREAM / GLOBAL / LEGACY), `LOG`, `TRACE` (ERROR / ESTIMATE), `CATALOG`, `CONNECTION_STATUS`, `SPEC`, `CONTROL`.
- Transport: newline-delimited JSON over stdin and stdout, with logs on stderr. A newer **socket mode** sends Protocol Buffers over Unix domain sockets with a "Bookkeeper" for control messages.
- Checkpoint semantics: **state counts as committed only after the destination echoes it back.** Destinations must return state messages in order.
- Sync modes:
  - source side: `full_refresh` and `incremental`, driven by a cursor field;
  - destination side: `append`, `append_dedup` and `overwrite`.

**Connector SDKs**
- The Python CDK, including the **low-code declarative YAML manifest**. Its top-level keys are `version`, `definitions`, `streams`, `check` and `spec`. Components include requester, paginator, record selector, partition router and incremental sync [SRC-064].
- The **Connector Builder UI** edits the same manifest and supports sources only [SRC-064][SRC-065].

**Schema discovery**
- The `discover` command [SRC-063].
- Profiling is not a core feature.

**Incremental and CDC**
- Cursor-based incremental per stream, with state checkpoints [SRC-063].
- Database CDC sources exist. Not separately verified for this report.

**Deployment**
- Self-managed "Core" or Airbyte Cloud [SRC-003].
- Self-managed users must manually update connector images, and syncs are not auto-paused past upgrade cutoffs [SRC-067].
- Each release publishes a list of breaking changes [SRC-070].

**Licence**
- Airbyte Core is **Elastic License 2.0 (ELv2)**. Airbyte's own connectors and the CDK "remain open-source" [SRC-066].

**Pricing (verified on airbyte.com)** [SRC-003]
- **Standard:** from **$20/month for 5 credits**, roughly 1 GB.
- **Plus credit packs:**

  | Credits | Monthly price |
  |---|---|
  | 40 | $189 |
  | 100 | $449 |
  | 250 | $999 |
  | 500 | $1,799 |
  | 1,000 | $3,199 |
  | 2,000 | $4,999 |

- **Pro and Enterprise Flex:** capacity-based on "Data Workers". Each runs about 3 concurrent syncs. Price is not published.
- **Trial:** 400 credits.
- The effective credit price falls from about $4.00 to about $2.50. This is a derived figure, not a published one.

**Complaints**
- Self-hosting is "a platform you run". One practitioner suggests budgeting about 0.5 FTE per quarter at scale [SRC-068].
- Community connectors crash or stall. This claim comes from a competitor (Estuary) and is *vendor-interested* [SRC-069].
- Upgrade and breaking-change churn [SRC-067][SRC-070].

**AI features**
- **Connector Builder AI Assist** prefills and configures fields from API docs or an OpenAPI spec [SRC-065].
- A Connector Builder MCP server is in development [SRC-065].

### 1.8 Fivetran (now Fivetran + dbt Labs)

**Corporate status**
- Acquired Tobiko Data (SQLMesh and SQLGlot) on 3 Sep 2025 [SRC-077][SRC-079].
- Completed the merger with dbt Labs on 1 Jun 2026 [SRC-078].

**Pipeline definition format**
- Managed SaaS configured through the UI and REST API. Schema selection is per connection.

**Connector model**
- 700+ managed connectors, closed source [SRC-001].
- The **Connector SDK** covers custom sources. It is a Python package that Fivetran hosts and runs, while the customer owns the logic [SRC-071][SRC-072].

**Staging and deployment**
- Fivetran-hosted by default.
- **Hybrid Deployment** places an agent inside the customer network. The agent makes outbound mTLS connections only, opens no inbound ports, and sends only metadata (logs and metrics) back [SRC-073][SRC-074].

**Incremental and CDC**
- Incremental by design: billing counts inserts, updates and deletes [SRC-001][SRC-002].
- **History mode** keeps SCD-style row history [SRC-002].

**Transformations**
- dbt Core integration [SRC-001].
- Transformation runs are billed as described below [SRC-001].

**Pricing (verified on fivetran.com)** [SRC-001][SRC-002]
- **Free plan:** 500,000 MAR, plus 5,000 model runs per month.
- **Billing unit:** MAR (monthly active rows) × a tiered rate. The rate falls with volume and differs by plan.
- **Examples from the vendor page** (Standard plan, company with 1–200 employees):

  | Connector | MAR | Monthly cost |
  |---|---|---|
  | Facebook Ads | 34,479 | $22.06 |
  | Marketo | 847,574 | $424.54 |

- **Transformations:**

  | Successful model runs per month | Price per run |
  |---|---|
  | 0–5,000 | free |
  | 5,001–30,000 | $0.01 |
  | 30,001–100,000 | $0.007 |
  | above 100,000 | $0.002 |

- **Annual discounts:** 5% to 22.6%.
- **Changes effective 1 Jan 2026** (pay-as-you-go immediately; annual contracts at renewal):
  - a **$5 minimum per standard connection** with 1–1M MAR;
  - **deletes count** toward paid MAR;
  - repeated updates in **history mode count**.
- **Change effective 1 Feb 2026:** Census was rebranded as "Activations", MAR-billed reverse ETL.

**Complaints**
- In March 2025 MAR calculation moved from account-wide to **per connection**, which removed cross-connector volume discounts [SRC-075][SRC-128].
- Reported increases of 35–70%, with some 2–4× anecdotes. These come from competitor blogs and are *vendor-interested* [SRC-075][SRC-076][SRC-128].
- Costs are hard to predict [SRC-128].

**AI features**
- The Connector SDK ships **AI plugins for coding agents**: Claude Code, Codex CLI, GitHub Copilot CLI and Gemini CLI. `fivetran init` detects installed agents [SRC-072].
- An "AI Connector Agent" handles publicly documented REST/JSON APIs [SRC-072].

### 1.9 dbt (dbt Core / dbt OSS / dbt platform)

**Pipeline definition format**
- SQL models plus YAML properties.
- **The DAG is inferred from `ref()` and `source()` calls**, and tests also use `ref()` [SRC-080].

**Transformation language**
- SQL templated with Jinja.
- dbt v2 rewrites the Jinja and SQL engine in Rust. Vendor claims cover faster parsing and linting [SRC-086].

**Connector model**
- Warehouse *adapters*. dbt does not extract or load data.

**Testing (a reference design)** [SRC-080]
- **Data tests** are `select` statements that return failing rows. A test with zero rows passes.
- **Generic tests** (`unique`, `not_null`, `accepted_values`, `relationships`) are declared in YAML under `data_tests:`. **Singular tests** are `.sql` files in `tests/`.
- `--store-failures` persists failing rows.
- **Unit tests** check model logic against fixed input rows, separately from data tests.

**Metadata and lineage**
- Manifest and run artifacts.
- dbt is an official OpenLineage integration [SRC-125].

**Deployment**
- A CLI that runs in-warehouse, with a minimal footprint, or the hosted dbt platform.

**Licence**
- **dbt OSS / dbt Core is Apache 2.0** [SRC-081].
- The Fusion engine was initially partly under ELv2 [SRC-082]. On 1 Jun 2026 the dbt-fusion repo was moved into dbt-core and **relicensed Apache 2.0**. A proprietary "dbt v2" distribution is governed by the dbt Product Licensing Agreement [SRC-081].
- dbt Core v2.0 (alpha) on the Fusion runtime is Apache 2.0 [SRC-078].

**Pricing (verified on getdbt.com)** [SRC-007]

| Plan | Price | Seats | Successful models per month | Projects |
|---|---|---|---|---|
| Developer | Free | 1 | 3,000 | not stated |
| Starter | **$100 per user per month** | 5 | 15,000 | 1 |
| Enterprise / Enterprise+ | Custom | Custom | 100,000 | 30 / unlimited |

The per-build overage price is not shown on that page.

**Complaints**
- Jinja is string templating that is unaware of SQL, so errors surface late. This view comes from SQLMesh and Tobiko, which are *vendor-interested* [SRC-083][SRC-084].
- Macros are "untestable" [SRC-085].
- Slow parse and compile on large projects. dbt Labs itself acknowledges this [SRC-086].

**AI features**
- Not verified for this report.

### 1.10 AWS Glue

**Pipeline definition format**
- PySpark or Scala scripts, Glue Studio visual ETL, or notebooks.

**Transformation language**
- Spark, using DynamicFrames or DataFrames.

**Connector model**
- Glue connections and the Data Catalog.
- **Crawlers** infer schemas into the catalog and are billed per DPU-hour [SRC-004].

**Incremental loads**
- **Job bookmarks** persist state so already-processed data is skipped [SRC-087][SRC-088].
- Bookmarks support JDBC sources and some S3 sources. S3 tracking uses object last-modified times [SRC-087][SRC-088].
- Bookmark keys can be set in the script [SRC-088].
- Resetting a bookmark does not delete target files [SRC-087].
- AWS documents common reasons that jobs reprocess data despite bookmarks [SRC-093].

**Data quality**
- Glue Data Quality tasks are billed per DPU-hour [SRC-004].

**Metadata and lineage**
- **Glue 5.0+ has built-in OpenLineage support** that feeds SageMaker Catalog (formerly DataZone) lineage [SRC-089].
- It covers Spark DataFrames only, not DynamicFrames, with a 300 KB event-size limit [SRC-090].

**Deployment**
- Serverless Spark, billed per second with a 1-minute minimum [SRC-004].

**Pricing (verified on aws.amazon.com)** [SRC-004]

| Item | Price |
|---|---|
| ETL jobs, standard | **$0.44 per DPU-hour** |
| ETL jobs, Flex | **$0.29 per DPU-hour** |
| Crawlers | $0.44 per DPU-hour |
| Data Catalog | first 1M objects and 1M requests free, then $1.00 per 100k objects per month |
| DataBrew jobs | $0.48 per node-hour |
| DataBrew interactive sessions | $1.00 per 30-minute session |
| Interactive sessions | minimum 2 DPUs, default 5 |

Prices vary by Region.

**Complaints**
- Job startup can take minutes. Reviewers on G2 and PeerSpot report 5–8 minute waits, although one PeerSpot reviewer disagrees [SRC-091][SRC-092].
- Unclear error messages and painful IAM debugging [SRC-091].
- Cost at scale [SRC-092].

**AI features**
- Not verified for this report.

### 1.11 Apache Beam (and Google Cloud Dataflow as a managed runner)

**Pipeline definition format**
- Code, with SDKs in Java, Python, Go, TypeScript (experimental) and **YAML** [SRC-097].

**Model** [SRC-097]
- A `Pipeline` contains immutable **PCollections**, which can be bounded or unbounded.
- **PTransforms** process PCollections. `ParDo` runs a `DoFn` per element.
- **Windowing**, based on element timestamps, plus triggers and watermarks.
- Runners execute the same graph on different back-ends.

**Testing** [SRC-098]
- `TestPipeline`, `Create` for in-memory inputs, and `PAssert` / `assert_that`.
- Local DirectRunner and PrismRunner.
- `TestStream` for unbounded pipelines, documented in a linked blog post.

**Connector model**
- I/O connectors are themselves PTransforms [SRC-097].

**Deployment**
- Runs on Flink, Spark or Dataflow.
- Apache Hop can run its pipelines through Beam runners [SRC-094][SRC-096].

**Licence**
- Apache 2.0, as an ASF project.

**Dataflow pricing (verified on cloud.google.com, figures as shown in search snippets)** [SRC-099]
- Batch vCPU about **$0.056/hour** in several US regions.
- FlexRS batch about **$0.0336/hour** in one regional table.
- Memory about $0.003557 per GiB-hour.
- Billed per second.
- A streaming figure of about $0.069 per vCPU-hour is **unverified**, from a third party.

**Complaints**
- Not separately researched. The conceptual complexity of windows and triggers is a commonly cited learning hurdle, but this is **not sourced here**.

### 1.12 Apache Hop

**Pipeline definition format**
- File-based **pipelines (`.hpl`)**, which process data, and **workflows (`.hwf`)**, which orchestrate [SRC-094].

**Metadata-driven design**
- Every reusable thing is a named *metadata object*: connections, run configurations, unit tests and servers.
- You "define once, reference by name". **Projects** and **environments** separate configuration such as dev, uat and prd [SRC-094].

**Engines**
- Native local, native remote (Hop Server), and **Beam-based engines** on Flink, Spark or Dataflow [SRC-094][SRC-096].

**Testing**
- First-class **pipeline unit tests**. Input data sets are injected and outputs are compared against **golden data sets** [SRC-095].
- Multiple tests can be defined per pipeline. Golden sets can be regenerated with the Data set output transform [SRC-095].

**Licence**
- Apache 2.0, as an ASF project.

**Complaints**
- Not separately researched.

**Relevance**
- Hop is the closest open-source analogue to a *metadata-driven, embeddable* engine. Note that it is JVM-based.

### 1.13 Dagster

**Corporate status**
- Prefect agreed to acquire Dagster Labs, announced in July 2026.
- Dagster and Dagster+ keep their names, OSS licences and roadmaps. Pricing is unchanged.
- Closing was "expected in the coming weeks" at the time of the FAQ [SRC-102][SRC-103][SRC-109].

**Model**
- **Software-defined assets**: an asset definition is code describing a persistent object, such as a table, file or model, and how to produce it.
- Asset definitions know their dependencies, which form the asset graph.
- Materialization runs the function and persists the result [SRC-100].

**Licence**
- Apache 2.0 [SRC-101].

**Lineage**
- An OpenLineage library converts Dagster events to OpenLineage events [SRC-105].

**Pricing (verified on dagster.io)** [SRC-008]

| Plan | Monthly fee | Per credit | Serverless compute | Limits |
|---|---|---|---|---|
| Solo | **$10** | $0.040 | $0.010/min | 1 user, 1 code location, 1 deployment |
| Starter | **$100** | $0.035 | $0.010/min | 3 users, 5 code locations, 1 deployment |
| Pro | custom | custom | custom | unlimited code locations and deployments |

- 1 asset materialization or op execution = 1 credit.
- Hybrid deployments carry no compute charge.

**Complaints**
- Steep learning curve. The asset model requires rethinking pipelines. The community is smaller than Airflow's [SRC-104].

### 1.14 Prefect

**Model**
- Python flows and tasks.
- In Prefect 3, every task run is governed by a **transaction**.
- Caching is built on top of transactions and needs result persistence, which is off by default. Results are stored by cache key [SRC-107][SRC-108].

**Licence**
- Apache 2.0 [SRC-106].

**Pricing (verified on prefect.io)** [SRC-009]

| Plan | Price | Users | Serverless compute |
|---|---|---|---|
| Hobby | free | 2 | 500 minutes per month |
| Starter | **$100/month** | 3 | 75 hours per month |
| Team | **$100 per user per month** | 4–8 | 225 hours per month |
| Enterprise | custom | 5+ | custom (adds SSO, SCIM, RBAC, PrivateLink) |

**Deployment**
- Hybrid model: a cloud control plane with customer workers ("bring your own compute"), or serverless [SRC-009].

**Complaints**
- Not separately researched.

### 1.15 Meltano and the Singer specification

**Singer spec (v0.3.0)** [SRC-110]
- Taps write JSON messages to stdout and targets read from stdin, so they compose with a pipe: `tap | target`.
- Messages: `SCHEMA` (JSON Schema, `key_properties`, `bookmark_properties`), `RECORD` and `STATE`. State holds per-stream bookmarks.
- Taps take a config file plus optional state and catalog files. `--discover` emits the catalog.
- Stream and field selection uses metadata:
  - non-discoverable metadata: `selected`, `replication-method` (`FULL_TABLE` / `INCREMENTAL` / `LOG_BASED`), `replication-key`;
  - discoverable metadata: `inclusion`, `valid-replication-keys`.

**Meltano**
- A project is defined by **`meltano.yml`**, with plugins (extractors, loaders, utilities) and environments.
- Plugins can inherit from, customise or shadow discoverable plugins.
- Run timestamps and incremental state are stored in a system database: SQLite by default, with PostgreSQL and MS SQL Server tested [SRC-111].

**Complaints**
- Not separately researched. Meltano itself publishes criticism of row-based pricing, which is *vendor-interested* [SRC-075].

### 1.16 dlt (dlthub)

**Model**
- An Apache 2.0 **Python library, "not a platform"**: `dlt.pipeline(...).run(...)` with `@dlt.resource` generators [SRC-112][SRC-114].
- It infers schemas, normalizes nested data, and supports incremental loading and 20+ destinations [SRC-112][SRC-114].
- It "can be deployed anywhere Python runs" [SRC-112].

**Schema contracts** [SRC-113]
- Contracts apply per entity: `tables`, `columns` and `data_type`.
- Modes:
  - `evolve`, the default;
  - `freeze`, which raises an error;
  - `discard_row`;
  - `discard_value`.
- Contracts can be set on a source, a resource or a run.

**Pricing**
- Open source (Apache 2.0) [SRC-114].
- Commercial offerings were not verified for this report.

**Relevance**
- dlt is the most direct conceptual peer to a small *embeddable* engine: a library-first design with a schema-contract policy model.

### 1.17 Estuary (Flow)

**Model**
- **Collections** are append-only sets of immutable JSON documents, validated against JSON Schema on every read and write [SRC-116].
- Catalog specs are written in **YAML or JSON** [SRC-116].
- **Derivations**, which are streaming transforms, can be written in SQLite, TypeScript or Python. Python is limited to private and BYOC data planes [SRC-115].
- TypeScript types are generated from schemas [SRC-116].

**Licence**
- The repo carries Apache and **BSL** licence files. The BSL governs "using Estuary outside the managed offering" [SRC-117].

**Pricing (verified on estuary.dev)** [SRC-010]
- **$0.50 per GB.** Data is counted at capture and again at each materialization.
- **Connector instances:** $100/month each for the first 6, then $50/month each after that.
- **Free tier:** 10 GB/month and 2 connectors.
- Private deployment and BYOC are available on Enterprise only.

**Complaints**
- Not separately researched.

### 1.18 Debezium

**Model**
- Log-based CDC source connectors [SRC-118].
- Deployment options:
  - **Kafka Connect**: the usual choice;
  - **Debezium Server**: a standalone application that writes to Kinesis, Pub/Sub, Pulsar and similar;
  - **Debezium Engine**: an *embedded Java library* inside your own application.

**Snapshots**
- **Incremental snapshots** are triggered by signals. The source signalling channel is enabled by default in 2.3, and a Kafka signal channel also exists [SRC-120].
- Incremental snapshots need write access to a signalling table unless the database supports read-only incremental snapshots [SRC-120].

**Outbox pattern**
- The **Outbox Event Router** SMT reads an outbox table with columns `id`, `aggregatetype`, `aggregateid`, `type` and `payload` [SRC-119].
- It routes by `aggregatetype` to `outbox.event.<type>` topics and keys messages by `aggregateid` for per-aggregate ordering [SRC-119].
- `id` supports consumer de-duplication [SRC-119].

**Licence**
- Open source. The licence file was not verified this session; Apache 2.0 is widely reported.

### 1.19 SQLMesh (Tobiko, now Fivetran)

**Model** [SRC-121]
- **Plans** compute directly and indirectly impacted models before applying a change, with chosen backfill ranges.
- **Virtual environments** promote non-production tables to production by repointing views, "no computation or data movement".
- **Unit tests** compare given inputs to expected outputs.
- **Audits** are SQL that must return zero rows.
- State is kept in a `sqlmesh` schema.

**Parser**
- SQLGlot transpiles between SQL dialects and detects errors [SRC-079].

**Ownership**
- Fivetran since September 2025 [SRC-077].
- Analysts flagged uncertainty about future licensing [SRC-079].

### 1.20 Redpanda Connect (formerly Benthos)

**Status**
- Redpanda acquired Benthos in May 2024 [SRC-124].

**Licence**
- The core and "99%+" of connectors are Apache 2.0 [SRC-123].
- **Enterprise connectors require a licence key** and are blocked when the key is missing or expired. Product-scoped licensing began in 4.78.0 [SRC-122].

**Transformation language**
- **Bloblang**, "a safe, fast, and powerful" mapping language. Mappings can be unit-tested with the built-in config testing [SRC-122 docs set].

**Relevance**
- A single declarative stream processor with a dedicated mapping DSL. It is a useful reference for a small engine's transform language.

---

## 2. Cross-product comparison tables

### 2.1 Definition format, transform language and connector protocol

| Product | Definition format | Transform language | Connector model / SDK | Sources |
|---|---|---|---|---|
| PowerCenter / IDMC | GUI; repository objects | Visual + expression language | Proprietary; Secure Agent runtime | SRC-021 |
| SSIS | `.dtsx` XML (visual) | Data flow + expressions + C# | .NET components; feature packs | SRC-030, SRC-027 |
| ADF / Fabric DF | JSON in Git; ARM deploy | Expressions; Spark data flows; Power Query | Linked services + IR | SRC-034, SRC-006 |
| Talend | Studio → generated Java | tMap / Java | Components compiled in | SRC-046 |
| NiFi | Canvas; JSON flow definitions in Git | Processors (Java/Python), EL | NAR processors; Python API | SRC-051, SRC-052 |
| PDI | `.ktr` / `.kjb` XML | Steps | Java plugins | SRC-061 |
| Airbyte | UI/API; YAML manifest (low-code) | Minimal (destination typing) | **Airbyte Protocol** (JSON over stdio / protobuf sockets) | SRC-063, SRC-064 |
| Fivetran | SaaS UI/API | dbt / SQLMesh | Closed connectors; Python Connector SDK | SRC-071 |
| dbt | SQL + YAML; DAG from `ref()` | SQL + Jinja | Warehouse adapters | SRC-080 |
| Glue | PySpark / Scala / visual | Spark | Connections + crawlers | SRC-004 |
| Beam | Code (Java/Python/Go/TS) + YAML | PTransforms | I/O transforms | SRC-097 |
| Hop | `.hpl` / `.hwf` + metadata objects | Transforms | Plugins; Beam engines | SRC-094 |
| Dagster | Python assets | Any (Python) | Integrations libs | SRC-100 |
| Prefect | Python flows / tasks | Any (Python) | Integrations libs | SRC-107 |
| Meltano / Singer | `meltano.yml` | n/a (dbt plugin) | **Singer spec** | SRC-110, SRC-111 |
| dlt | Python library | Python | Resources / sources (Python) | SRC-112 |
| Estuary | YAML/JSON catalog | SQLite / TypeScript / Python derivations | Capture / materialize connectors | SRC-115, SRC-116 |
| Debezium | Connector config (properties/JSON) | SMTs | Kafka Connect / Server / Engine | SRC-118 |
| SQLMesh | SQL / Python models | SQL (SQLGlot) | Engine adapters | SRC-121 |
| Redpanda Connect | Config | Bloblang | Input / output plugins | SRC-122 |

### 2.2 Lineage, testing, incremental and deployment

| Product | OpenLineage | Testing | Incremental / CDC | Footprint |
|---|---|---|---|---|
| PowerCenter / IDMC | Not found [SRC-026] | Not first-class | Mass Ingestion (IPU) | Server or SaaS + Secure Agent |
| SSIS | Not found | Not first-class | CDC removed in 2025 [SRC-028] | SQL Server / Azure-SSIS IR |
| ADF / Fabric | Not verified | Not first-class | Copy job incremental meter [SRC-041] | PaaS; 8-vCore minimum for data flows |
| NiFi | Not verified; native provenance | Java harness | Stateful processors | JVM cluster + 3 repositories |
| Airbyte | Not verified | Connector acceptance tests (not verified) | Cursor state; CDC sources | Kubernetes / Docker or Cloud |
| Fivetran | Not verified | n/a | MAR-based incremental; history mode | SaaS / Hybrid agent |
| dbt | **Yes** (official) [SRC-125] | **Data + unit tests** | Incremental models | CLI |
| Glue | **Yes** (Glue 5.0+) [SRC-089] | Data Quality | Job bookmarks | Serverless Spark |
| Beam | Not verified | **TestPipeline / PAssert** | Windowing / watermarks | Runner-dependent |
| Hop | Not verified | **Golden data sets** | — | JVM; local or Beam |
| Dagster | **Yes** (library) [SRC-105] | Asset checks (not verified) | Partitions (not verified) | Python + daemon / Dagster+ |
| SQLMesh | Not verified | **Unit tests + audits** | Interval state | CLI + state schema |
| Debezium | Not verified | — | **Log-based CDC**; incremental snapshots | Kafka Connect / Server / embedded |

### 2.3 Published pricing summary

| Product | Unit | Headline price | Status |
|---|---|---|---|
| Fivetran | MAR, tiered; model runs | Free 500k MAR; $5 per connection minimum (1–1M MAR); model runs $0.01–$0.002 | **Verified** [SRC-001][SRC-002] |
| Airbyte Cloud | Credits / Data Workers | $20 for 5 credits; Plus from $189 for 40 credits up to $4,999 for 2,000 | **Verified** [SRC-003] |
| ADF | Activity runs / DIU-hour / vCore-hour | $1 per 1k runs; $0.25 per DIU-hour; $0.27325 per vCore-hour GP | **Verified** (Azure price API) [SRC-006] |
| Fabric DF | CU-hours | Copy 1.5 CU-h; orchestration 0.0056 CU-h per run | **Verified** (meters); $ rate illustrative [SRC-040][SRC-042] |
| Glue | DPU-hour | $0.44 (Flex $0.29) | **Verified** [SRC-004] |
| Dataflow (Beam) | vCPU-hour | ~$0.056 batch | Verified via vendor-page snippet [SRC-099] |
| dbt | Seat + models | $100 per user per month (Starter) | **Verified** [SRC-007] |
| Dagster+ | Credits | $10 / $100 per month; $0.04 / $0.035 per credit | **Verified** [SRC-008] |
| Prefect Cloud | Plan / seat | $100 per month; $100 per user per month | **Verified** [SRC-009] |
| Estuary | GB + connector | $0.50 per GB; $100 / $50 per connector per month | **Verified** [SRC-010] |
| Informatica IDMC | IPU | No list price; £74,999 minimum (G-Cloud) | **Unverified** [SRC-015][SRC-016] |
| Qlik Talend Cloud | Data moved | Starter $6,000 per year for 50 GB per month (AWS Marketplace) | **Unverified** [SRC-045] |
| SSIS (Azure-SSIS IR) | VM-hour | D4 v3 Standard $0.969/h | **Verified** (Azure price API) [SRC-006] |
| Pentaho | Subscription | Not published | **Unverified** |

---

## 3. (a) Architectural patterns worth adopting in an embeddable F# engine

Each pattern lists its evidence, followed by **F# guidance**.

1. **A process- or boundary-separated connector protocol, using Singer or Airbyte messages.**
   - Evidence: connectors talk only through a small closed set of typed messages, `SCHEMA` / `RECORD` / `STATE` in Singer and the `AirbyteMessage` union in Airbyte. Transport is stdio JSON lines, and Airbyte adds protobuf over Unix sockets for throughput [SRC-063][SRC-110].
   - F# guidance: model the messages as a discriminated union.
   - Support three transports:
     - in-process, using `IAsyncEnumerable` / `TaskSeq`;
     - out-of-process, using stdio JSONL, which makes **existing Singer taps and Airbyte connectors reusable for free**;
     - binary transport, for speed.
   - Implement `spec` / `check` / `discover` / `read` / `write` as the connector interface.

2. **State committed only on destination acknowledgement.**
   - Evidence: Airbyte treats a state checkpoint as committed only when the destination echoes it back in order [SRC-063].
   - Evidence: Debezium keys messages by aggregate and offers dedup IDs [SRC-119].
   - F# guidance: this provides exactly-once-*effective* resumption. Make the checkpoint store pluggable: file, SQLite or the destination itself, following Meltano's system DB with SQLite by default [SRC-111].

3. **A declarative connector manifest for HTTP APIs.**
   - Evidence: Airbyte's low-code YAML manifest is built from composable requester, paginator, record-selector, partition-router and incremental components [SRC-064].
   - F# guidance: a typed manifest, in YAML or JSON with a JSON Schema, covers most REST sources without code. It is also the right target for AI generation: an LLM fills a schema-validated spec instead of writing code [SRC-065][SRC-072].

4. **Tests-as-code and a DAG inferred from references.**
   - Evidence: in dbt, data tests are queries that return failing rows [SRC-080].
   - Evidence: unit tests run on fixed inputs (dbt, SQLMesh) [SRC-080][SRC-121].
   - Evidence: the DAG comes from `ref()` rather than hand-wired edges [SRC-080].
   - Evidence: Hop provides golden data sets per pipeline [SRC-095].
   - Evidence: Beam provides `TestPipeline` + `PAssert` with in-memory `Create` inputs [SRC-098].
   - F# guidance: provide `Expecto`/`xUnit` helpers that run a pipeline against in-memory sources and assert on outputs, and infer dependencies from typed references.

5. **Plan, apply and virtual environments.**
   - Evidence: SQLMesh computes impact before execution, and its virtual environments promote by pointer swap with no data movement [SRC-121].
   - F# guidance: a dry-run "plan" that diffs schema and spec against current state is cheap to build and greatly improves safety.

6. **Software-defined assets.**
   - Evidence: Dagster declares *what should exist*, and materialization is a function of upstream assets [SRC-100].
   - F# guidance: even without an orchestrator, have each pipeline output declare an asset key. This makes lineage, freshness and selective re-runs natural.

7. **Schema contracts as policy.**
   - Evidence: dlt's `evolve` / `freeze` / `discard_row` / `discard_value` modes apply to tables, columns and types [SRC-113].
   - Evidence: Estuary validates against JSON Schema on both read and write [SRC-116].
   - F# guidance: make the contract a first-class, per-stream setting, and use F# types or a JSON Schema at the boundary.

8. **A provenance repository and replay.**
   - Evidence: NiFi's immutable content store plus provenance events allow lineage and replay of any FlowFile while its content is retained [SRC-050].
   - F# guidance: a lightweight equivalent is an append-only event log of batch IDs → input offsets → output locations. It enables replay and audit without NiFi's weight.

9. **Emit OpenLineage events.**
   - Evidence: OpenLineage is the de facto interchange, with official integrations for Airflow, Spark, dbt, Flink, Great Expectations and Trino [SRC-125].
   - Evidence: AWS Glue 5.0 [SRC-089] and Dagster, through a library [SRC-105], also emit it.
   - F# guidance: emitting `RunEvent` START / COMPLETE / FAIL with dataset facets is a small effort for large ecosystem interoperability. Consumers include Marquez, DataHub, OpenMetadata, Google Knowledge Catalog and IBM watsonx.data [SRC-026][SRC-127].

10. **A unified bounded and unbounded model.**
    - Evidence: Beam's PCollection, windowing and runner abstraction separate *what* from *where* [SRC-097].
    - Evidence: Hop reuses this idea by delegating pipelines to Beam runners [SRC-094].
    - F# guidance: design the core around a stream abstraction, so batch is a bounded stream. Keep execution engines pluggable.

11. **Metadata-driven, define-once objects with projects and environments.**
    - Evidence: Hop's named metadata objects, such as connections and run configurations, are referenced by name and overridden per environment [SRC-094].
    - F# guidance: separate the spec from environment bindings and secrets.

12. **An embeddable CDC library plus the outbox pattern.**
    - Evidence: the Debezium Engine runs inside an application without Kafka [SRC-118].
    - Evidence: the outbox router solves the dual-write problem with a simple table contract [SRC-119].
    - F# guidance: support an outbox-table source mode with the same column contract.

13. **Control-plane / data-plane split for hosted variants.**
    - Evidence: Fivetran Hybrid uses outbound-only mTLS and sends metadata only [SRC-073][SRC-074].
    - Evidence: Informatica's Secure Agent uses outbound HTTPS/443 [SRC-021].
    - F# guidance: if a hosted UI is ever offered, keep data in the embedding process.

14. **Transactions, caching and idempotency keys.**
    - Evidence: Prefect 3 gives each task run a transaction and cache key, with persistence-backed result reuse [SRC-107][SRC-108].
    - F# guidance: make every step idempotent by key.

15. **A dedicated small mapping DSL.**
    - Evidence: Redpanda Connect's Bloblang is a focused, testable mapping language [SRC-122].
    - F# guidance: F# computation expressions or quotations could give a typed equivalent.

## 4. (b) Features that exist mainly because of historical product complexity

These are features to avoid or to treat as legacy.

1. **GUI-only artifacts serialized as designer-coupled XML.**
   - Examples: SSIS `.dtsx` with lineage IDs and layout in the file, and PDI `.ktr`/`.kjb` [SRC-030][SRC-032][SRC-061].
   - Consequences: merges break flows. Teams fall back to *pessimistic locking* or treat packages "like executables" [SRC-032]. Even ADF's JSON needs ARM templating and linked templates at scale [SRC-034][SRC-035].
2. **Code-generation runtimes.**
   - Talend compiles jobs to Java and hits the JVM 64 KB method limit [SRC-046].
   - Its Studio IDE needs multi-gigabyte heaps [SRC-047][SRC-048].
3. **Mandatory per-engine runtime clusters and agents.**
   - ADF Mapping Data Flows need a minimum 8-vCore Spark cluster [SRC-005].
   - Glue runs serverless Spark with minute-scale startup [SRC-091][SRC-092].
   - IDMC requires a Secure Agent [SRC-021].
   - Azure-SSIS IR VMs cost from $0.58 to $32+ per hour [SRC-006].
4. **Multiple runtime flavours of one product.**
   - Examples: Azure, self-hosted, managed-VNET and SSIS integration runtimes, each with different meters [SRC-006]; Informatica's hosted and secure agents [SRC-021].
5. **Repository-versus-file split modes.**
   - PDI forbids mixing file and repository storage in one project [SRC-061].
   - NiFi needed a separate Registry service until Git clients arrived in 2.x [SRC-053].
6. **Opaque capacity-unit pricing.**
   - Examples: IPUs metered per "scaler" [SRC-014], Fabric CU [SRC-040] and Airbyte "credits" or "Data Workers" [SRC-003].
   - These abstractions exist to price many heterogeneous services together. They make cost hard to predict, and [SRC-036] cites ADF cost estimation as a con.
7. **Bundled vendor-specific CDC add-ons.**
   - Attunity CDC components in SSIS were deprecated and then removed [SRC-028].
   - The Oracle connector was dropped [SRC-029].
8. **Ever-growing deprecation lists.**
   - Examples: SSIS 32-bit mode, the legacy SSIS service and the SDS connection type [SRC-027].
   - Legacy "LEGACY" state type retained in the Airbyte protocol [SRC-063].

## 5. (c) Observed failure modes and complaints across the category

| # | Failure mode | Examples (sources) |
|---|---|---|
| 1 | **Pricing surprise / unpredictability** from row- or unit-based metering; changes mid-contract | Fivetran per-connection MAR (Mar 2025), $5 minimum and delete counting (Jan 2026) [SRC-002][SRC-075][SRC-128]; ADF cost estimation [SRC-036]; Glue cost at scale [SRC-092]; Informatica "expensive and inflexible" [SRC-024] |
| 2 | **Poor debuggability / vague errors** | ADF generic errors, debug vs monitor mismatch [SRC-036][SRC-037]; Glue unclear errors, IAM [SRC-091]; dbt Jinja errors found only at run [SRC-083] |
| 3 | **Slow startup / heavyweight tooling** | Glue minutes-long start [SRC-091][SRC-092]; Talend Studio memory and startup [SRC-048]; NiFi memory/CPU [SRC-055] |
| 4 | **Connector fragility and upgrade churn** | Airbyte manual image updates, breaking-change lists, community connector stalls [SRC-067][SRC-069][SRC-070] |
| 5 | **Version control / collaboration friction** | SSIS merges [SRC-031][SRC-032]; ADF ARM template limits [SRC-035]; NiFi metadata readability [SRC-054] |
| 6 | **Steep learning curves** | PowerCenter [SRC-023][SRC-025], NiFi [SRC-054], Dagster [SRC-104] |
| 7 | **Open-source rug-pulls / licence shifts** | Talend Open Studio retired [SRC-043]; Pentaho CE restricted at 10.2 [SRC-058]; Airbyte ELv2 [SRC-066]; Redpanda Connect enterprise key gating [SRC-122]; Estuary BSL [SRC-117]; dbt Fusion ELv2 → later Apache 2.0 [SRC-081][SRC-082] |
| 8 | **Forced platform migrations** | PowerCenter end of standard support (Mar 2026) → IDMC [SRC-011][SRC-012]; SSIS CDC removal [SRC-028] |
| 9 | **Incremental-state correctness bugs** | Glue bookmark reprocessing knowledge-centre article [SRC-093]; Airbyte state commit semantics required to avoid skips [SRC-063] |
| 10 | **Vendor consolidation uncertainty** | SQLMesh licence questions after the Fivetran deal [SRC-079]; open questions on dbt OSS commitment after the merger [SRC-078]; Dagster under Prefect [SRC-103] |
| 11 | **Self-hosting operational burden** | Airbyte about 0.5 FTE per quarter [SRC-068]; NiFi capacity planning [SRC-055] |

## 6. Implications for an embeddable F# engine (synthesis)

- **Positioning gap.** No surveyed product is all of the following:
  - (a) a permissively licensed *library*;
  - (b) in .NET;
  - (c) protocol-compatible with Singer and Airbyte connectors;
  - (d) shipped with tests-as-code and OpenLineage.

  dlt is the closest analogue, but it is Python [SRC-112][SRC-114]. Debezium Engine and Hop are JVM [SRC-118][SRC-094].
- **Minimum viable differentiators:**
  - a typed spec (JSON or YAML, plus F# DSL) that diffs cleanly in Git, which is the lesson from failure mode 5;
  - Singer and Airbyte protocol adapters;
  - ack-based checkpoints;
  - schema-contract modes;
  - golden-dataset tests;
  - a plan / dry-run step;
  - OpenLineage emission;
  - an append-only run/provenance log.
- **AI-assist design.** Vendor AI features produce opaque artifacts: CLAIRE mappings, Fabric pipelines, Airbyte manifests and Fivetran SDK code [SRC-018][SRC-038][SRC-065][SRC-072]. A strongly typed, JSON-Schema-validated spec is a better LLM target, because it can be validated, unit-tested and dry-run planned before execution.
- **Pricing lesson.** If commercialised, prefer predictable pricing, for example per instance or per seat, over row- or credit-metering. Category complaints concentrate on metering surprises [SRC-075][SRC-036].

---

## 7. Source list

All sources were accessed on **2026-11-26**.

### 7.1 Fivetran, Airbyte, cloud pricing pages and orchestrator pricing (SRC-001 to SRC-010)

- **SRC-001** Fivetran Pricing. https://www.fivetran.com/pricing
- **SRC-002** Fivetran docs, 2026 Pricing Updates. https://fivetran.com/docs/usage-based-pricing/pricing-updates/2026-pricing-updates
- **SRC-003** Airbyte Pricing. https://airbyte.com/pricing
- **SRC-004** AWS Glue Pricing. https://aws.amazon.com/glue/pricing/
- **SRC-005** Azure Data Factory pipeline pricing page. https://azure.microsoft.com/en-us/pricing/details/data-factory/data-pipeline/
- **SRC-006** Azure Retail Prices API, query `serviceName eq 'Azure Data Factory v2' and armRegionName eq 'eastus' and priceType eq 'Consumption'`. https://prices.azure.com/api/retail/prices
- **SRC-007** dbt Pricing. https://www.getdbt.com/pricing
- **SRC-008** Dagster Pricing. https://dagster.io/pricing
- **SRC-009** Prefect Pricing. https://www.prefect.io/pricing
- **SRC-010** Estuary Pricing. https://estuary.dev/pricing/

### 7.2 Informatica (SRC-011 to SRC-026)

- **SRC-011** Informatica downloads / PowerCenter lifecycle. https://www.informatica.com/download.html
- **SRC-012** CData, "The Sun is Setting on PowerCenter Support". https://www.cdata.com/blog/sun-sets-on-powercenter-whats-next
- **SRC-013** Ksolves, "PowerCenter End of Support". https://www.ksolves.com/blog/big-data/powercenter-end-of-support
- **SRC-014** Informatica blog, Volume Tier Pricing and Flex IPU. https://www.informatica.com/blogs/announcing-volume-tier-pricing-and-flex-ipu-consumption-based-pricing-for-informatica-intelligent-data-management-cloud.html
- **SRC-015** Informatica IDMC consumption pricing page. https://www.informatica.com/products/cloud-integration/pricing.html
- **SRC-016** UK G-Cloud 15 Informatica pricing document (search summary only, unverified). https://assets.applytosupply.digitalmarketplace.service.gov.uk/g-cloud-15/documents/703188/592589319296837-pricing-document-2026-01-29-1612.pdf
- **SRC-017** Salesforce, "Salesforce Completes Acquisition of Informatica" (18 Nov 2025). https://www.salesforce.com/news/press-releases/2025/11/18/salesforce-completes-acquisition-of-informatica/
- **SRC-018** Informatica blog, Agentic goal-driven data management with CLAIRE GPT. https://www.informatica.com/blogs/introducing-agentic-goal-driven-data-management-with-claire-gpt.html
- **SRC-019** Informatica news release, AI-powered Cloud Integration and MDM capabilities (2 Apr 2025). https://www.informatica.com/about-us/news/news-releases/2025/04/20250402-informatica-introduces-new-ai-powered-cloud-integration-and-master-data-management-capabilities.html
- **SRC-020** Informatica CLAIRE promotion sign-up page. https://www.informatica.com/DEModSignUp
- **SRC-021** Informatica docs, Runtime Environments > Secure Agents. https://onlinehelp.informatica.com/IICS/dev/admin/en/gg-iics-rte/Secure_Agents.html
- **SRC-022** Informatica 2025 IDMC Security Architecture Whitepaper. https://trust.informatica.com/content/dam/informatica-trust/generic/2025_idmc_security_architecture_whitepaper_3.pdf
- **SRC-023** G2, Informatica PowerCenter reviews. https://www.g2.com/products/informatica-powercenter/reviews
- **SRC-024** PeerSpot, Informatica PowerCenter pros and cons. https://origin.peerspot.com/products/informatica-powercenter-pros-and-cons
- **SRC-025** SelectHub, Informatica PowerCenter. https://www.selecthub.com/p/etl-tools/informatica-powercenter/
- **SRC-026** Informatica, "Data Lineage in CDGC, Part 2" (slides). https://www.informatica.com/content/dam/informatica-cxp/techtuesdays-slides-pdf/Data%20Lineage%20in%20CDGC%20A%20Practical%20Guide%20to%20Key%20Categories%20and%20Setup%20Approaches%20-%20Part%202.pdf

### 7.3 Microsoft: SSIS, ADF and Fabric (SRC-027 to SRC-042)

- **SRC-027** Microsoft Learn, What's new in Integration Services in SQL Server 2025. https://learn.microsoft.com/en-us/sql/integration-services/what-s-new-in-integration-services-in-sql-server-2025
- **SRC-028** Microsoft SQL Server Blog, SSIS CDC by Attunity deprecations (28 Feb 2024). https://www.microsoft.com/en-us/sql-server/blog/2024/02/28/sql-server-integration-services-ssis-change-data-capture-attunity-feature-deprecations/
- **SRC-029** Microsoft SQL Server Blog, SSIS Microsoft Connector for Oracle deprecation (21 Jan 2025). https://www.microsoft.com/sql-server/blog/2025/01/21/sql-server-integration-services-ssis-microsoft-connector-for-oracle-deprecation
- **SRC-030** Microsoft Tech Community, Package format changes in SQL Server Denali. https://techcommunity.microsoft.com/blog/ssis/package-format-changes-in-sql-server-denali/387953
- **SRC-031** MSSQLTips, Git merge conflict SSIS projects. https://www.mssqltips.com/sqlservertip/6683/git-merge-conflict-ssis-projects
- **SRC-032** Stack Overflow, "How do I merge SSIS package files?". https://stackoverflow.com/questions/5468151/how-do-i-merge-ssis-package-files
- **SRC-033** Directions on Microsoft, SQL Server Integration Services roadmap. https://www.directionsonmicrosoft.com/roadmaps/ref/sql-server-integration-services-roadmap/
- **SRC-034** Microsoft Learn, Continuous integration and delivery in Azure Data Factory. https://learn.microsoft.com/en-us/azure/data-factory/continuous-integration-delivery
- **SRC-035** Microsoft Learn, Linked Resource Manager templates with CI/CD. https://learn.microsoft.com/en-us/azure/data-factory/continuous-integration-delivery-linked-templates
- **SRC-036** G2, Azure Data Factory reviews. https://www.g2.com/products/azure-data-factory/reviews
- **SRC-037** SQLServerCentral, "Azure Data Factory pipeline debugging fails with BadRequest". https://www.sqlservercentral.com/blogs/azure-data-factory-pipeline-debugging-fails-with-badrequest
- **SRC-038** Microsoft Learn, Copilot for Fabric Data Factory, get started. https://learn.microsoft.com/en-us/fabric/data-factory/copilot-fabric-data-factory-get-started
- **SRC-039** Microsoft Fabric Blog, AI-powered development with Data Factory. https://blog.fabric.microsoft.com/en-US/blog/ai-powered-development-with-data-factory-microsoft-fabric/
- **SRC-040** Microsoft Learn, Data pipelines pricing for Fabric Data Factory. https://learn.microsoft.com/en-us/fabric/data-factory/pricing-pipelines
- **SRC-041** Microsoft Learn, Copy job pricing. https://learn.microsoft.com/fabric/data-factory/pricing-copy-job
- **SRC-042** Microsoft Learn, Pricing scenario: load 1 TB Parquet to Data Warehouse. https://learn.microsoft.com/en-us/fabric/data-factory/pricing-scenario-load-1-tb-parquet-to-data-warehouse

### 7.4 Qlik Talend (SRC-043 to SRC-049)

- **SRC-043** Qlik, Talend Open Studio retirement page. https://www.qlik.com/us/products/talend-open-studio
- **SRC-044** Qlik Talend Cloud Plans and Pricing. https://www.qlik.com/us/pricing/data-integration-products-pricing
- **SRC-045** AWS Marketplace, Qlik Talend Cloud Starter listing (search summary only, unverified). https://aws.amazon.com/marketplace/pp/prodview-yvole2ix5rkfq
- **SRC-046** Qlik Help, Preventing code generation errors caused by the 65 KB limit. https://help.qlik.com/talend/en-US/code-generation-prevent-error/8.0/how-to-prevent-errors-in-code-generation-caused-by-65-kb-limit
- **SRC-047** Qlik Help, Optimizing Talend Studio performance. https://help.qlik.com/talend/en-US/installation-guide-linux/Cloud/optimizing-talend-studio-performance
- **SRC-048** Capterra, Talend Open Studio reviews. https://www.capterra.com/p/246747/Talend-Open-Studio/reviews
- **SRC-049** Qlik Community, Download Talend Open Studio thread. https://community.qlik.com/t5/Installing-and-Upgrading/Download-Talend-Open-Studio/td-p/2470265

### 7.5 Apache NiFi (SRC-050 to SRC-056)

- **SRC-050** Apache NiFi In Depth. https://nifi.apache.org/docs/nifi-docs/html/nifi-in-depth.html
- **SRC-051** Apache NiFi Python Developer's Guide (2.0.0-M1). https://nifi.apache.org/documentation/nifi-2.0.0-M1/html/python-developer-guide.html
- **SRC-052** Apache NiFi, GitHubFlowRegistryClient component. https://nifi.apache.org/components/org.apache.nifi.github.GitHubFlowRegistryClient/
- **SRC-053** Stackable docs, NiFi Flow Versioning. https://docs.stackable.tech/home/25.7/nifi/usage_guide/flow-versioning/
- **SRC-054** PeerSpot, Apache NiFi pros and cons. https://peerspot.com/products/apache-nifi-pros-and-cons
- **SRC-055** Kestra, Apache NiFi alternatives (vendor-interested). https://kestra.io/resources/data/apache-nifi-alternatives
- **SRC-056** Xebia, "Apache NiFi: why do data engineers love it and hate it". https://xebia.com/blog/apache-nifi-why-do-data-engineers-love-it-and-hate-it-at-the-same-time-blog-series-introduction/

### 7.6 Pentaho (SRC-057 to SRC-062)

- **SRC-057** Pentaho, Statement of Direction. https://pentaho.com/statement-of-direction/
- **SRC-058** Wikipedia, Pentaho. https://en.wikipedia.org/wiki/Pentaho
- **SRC-059** Hitachi Vantara, Pentaho Community Edition page. https://www.hitachivantara.com/de-de/products/pentaho-platform/data-integration-analytics/pentaho-community-edition.html
- **SRC-060** Hitachi Vantara docs, Work with transformations (PDI 9.5). https://help.hitachivantara.com/Documentation/Pentaho/Data_Integration_and_Analytics/9.5/Products/Work_with_transformations
- **SRC-061** O'Reilly / Packt, Pentaho Data Integration Beginner's Guide, Appendix B: Pan and Kitchen. https://www.oreilly.com/library/view/pentaho-data-integration/9781782165040/apb.html
- **SRC-062** PeerSpot, What needs improvement with Pentaho Data Integration. https://origin.peerspot.com/questions/what-needs-improvement-with-pentaho-data-integration

### 7.7 Airbyte (SRC-063 to SRC-070)

- **SRC-063** Airbyte docs, Airbyte Protocol. https://docs.airbyte.com/platform/understanding-airbyte/airbyte-protocol
- **SRC-064** Airbyte docs, Low-code CDK overview. https://docs.airbyte.com/platform/connector-development/config-based/low-code-cdk-overview
- **SRC-065** Airbyte docs, Connector Builder AI Assist. https://docs.airbyte.com/platform/connector-development/connector-builder-ui/ai-assist
- **SRC-066** Airbyte docs, License FAQ. https://docs.airbyte.com/platform/developer-guides/licenses/license-faq
- **SRC-067** Airbyte docs, Connector updates. https://docs.airbyte.com/platform/managing-airbyte/connector-updates
- **SRC-068** Enterprise DNA, Practitioner Airbyte review. https://enterprisedna.co/resources/blog/practitioner-airbyte-review
- **SRC-069** Estuary blog, Airbyte sync job failures in production (vendor-interested). https://estuary.dev/blog/airbyte-sync-jobs-failure-production/
- **SRC-070** Airbyte docs, Breaking change list. https://docs.airbyte.com/release_notes/breaking-changes

### 7.8 Fivetran and dbt (SRC-071 to SRC-086)

- **SRC-071** Fivetran docs, Connector SDK. https://fivetran.com/docs/connector-sdk
- **SRC-072** Fivetran docs, Building Custom Connectors with AI Agents. https://fivetran.com/docs/connector-sdk/building-connectors/ai-tools
- **SRC-073** Fivetran docs, Hybrid Deployment. https://fivetran.com/docs/core-concepts/deployment-models/hybrid-deployment
- **SRC-074** Fivetran docs, What data does Fivetran receive from my local environment? https://fivetran.com/docs/deployment-models/hybrid-deployment/troubleshooting/receive-data-from-local
- **SRC-075** Meltano blog, The hidden business cost of row-based ETL pricing (vendor-interested). https://meltano.com/blog/the-hidden-business-cost-of-row-based-etl-pricing-when-growth-becomes-a-liability
- **SRC-076** Definite blog, Fivetran bill doubled (vendor-interested). https://www.definite.app/blog/fivetran-bill-doubled
- **SRC-077** Fivetran blog, Fivetran acquires Tobiko Data. https://www.fivetran.com/blog/fivetran-acquires-tobiko-data-to-power-enterprise-grade-transformations
- **SRC-078** Fivetran press, Fivetran and dbt Labs complete merger (1 Jun 2026). https://www.fivetran.com/press/fivetran-dbt-labs-complete-merger-to-create-the-data-infrastructure-for-trusted-ai-agents
- **SRC-079** TechTarget, Fivetran's Tobiko Data acquisition aids data transformation. https://www.techtarget.com/searchdatamanagement/news/366630327/Fivetrans-Tobiko-Data-acquisition-aids-data-transformation
- **SRC-080** dbt docs, Data tests. https://docs.getdbt.com/docs/build/data-tests
- **SRC-081** dbt Licensing FAQ. https://www.getdbt.com/licenses-faq
- **SRC-082** dbt blog, New code, new license: the dbt Fusion engine. https://www.getdbt.com/blog/new-code-new-license-understanding-the-new-license-for-the-dbt-fusion-engine
- **SRC-083** SQLMesh docs, Comparisons (vendor-interested). https://sqlmesh.readthedocs.io/en/latest/comparisons/
- **SRC-084** Tobiko blog, Traps and pitfalls of using SQL with Jinja (vendor-interested). https://tobikodata.com/blog/traps-and-pitfalls-of-using-sql-with-jinja
- **SRC-085** Benn Stancil, "How dbt fails". https://benn.substack.com/p/how-dbt-fails
- **SRC-086** dbt Developer Blog, Faster project parsing with Rust. https://docs.getdbt.com/blog/faster-project-parsing-with-rust

### 7.9 AWS Glue and lineage (SRC-087 to SRC-093)

- **SRC-087** AWS Glue docs, Tracking processed data using job bookmarks. https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html
- **SRC-088** AWS Glue docs, Using job bookmarks. https://docs.aws.amazon.com/glue/latest/dg/programming-etl-connect-bookmarks.html
- **SRC-089** AWS Big Data Blog, Capture data lineage from dbt, Apache Airflow and Apache Spark with Amazon SageMaker. https://aws.amazon.com/blogs/big-data/capture-data-lineage-from-dbt-apache-airflow-and-apache-spark-with-amazon-sagemaker
- **SRC-090** AWS docs, Automate lineage capture from tools (SageMaker Unified Studio). https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/datazone-data-lineage-automate-capture-from-tools.html
- **SRC-091** G2, AWS Glue reviews. https://www.g2.com/products/aws-glue/reviews
- **SRC-092** PeerSpot, AWS Glue pros and cons. https://peerspot.com/products/aws-glue-pros-and-cons
- **SRC-093** AWS Knowledge Center, Glue reprocesses data with job bookmarks enabled. https://aws.amazon.com/premiumsupport/knowledge-center/glue-reprocess-data-job-bookmarks-enabled/

### 7.10 Apache Hop, Apache Beam and Dataflow (SRC-094 to SRC-099)

- **SRC-094** Apache Hop manual, Hop Concepts. https://hop.apache.org/manual/latest/getting-started/hop-concepts.html
- **SRC-095** Apache Hop manual, Pipeline Unit Testing. https://hop.apache.org/manual/next/pipeline/pipeline-unit-testing.html
- **SRC-096** Apache Hop manual, Getting started with Apache Beam. https://hop.apache.org/manual/next/pipeline/beam/getting-started-with-beam.html
- **SRC-097** Apache Beam Programming Guide. https://beam.apache.org/documentation/programming-guide/
- **SRC-098** Apache Beam, Test Your Pipeline. https://beam.apache.org/documentation/pipelines/test-your-pipeline/
- **SRC-099** Google Cloud, Dataflow pricing. https://cloud.google.com/dataflow/pricing

### 7.11 Dagster and Prefect (SRC-100 to SRC-109)

- **SRC-100** Dagster docs, Assets. https://dagster.io/docs/guides/build/assets
- **SRC-101** GitHub, dagster-io/dagster (licence). https://github.com/dagster-io/dagster
- **SRC-102** Dagster blog, Prefect is acquiring Dagster. https://dagster.io/blog/prefect-is-acquiring-dagster
- **SRC-103** Dagster Customer FAQ: Prefect Acquisition. https://dagster.io/dagster-customer-faq
- **SRC-104** Atlan, Dagster vs Airflow. https://atlan.com/dagster-vs-airflow/
- **SRC-105** OpenLineage Ecosystem page (Dagster integration). https://openlineage.github.io/ecosystem
- **SRC-106** GitHub, PrefectHQ/prefect (licence). https://github.com/PrefectHQ/prefect
- **SRC-107** Prefect docs, Transactions. https://docs.prefect.io/v3/develop/transactions
- **SRC-108** Prefect docs, Task caching. https://docs.prefect.io/v3/develop/task-caching
- **SRC-109** The New Stack, Prefect acquires Dagster orchestrator. https://thenewstack.io/prefect-acquires-dagster-orchestrator/

### 7.12 Meltano/Singer, dlt, Estuary, Debezium, SQLMesh and Redpanda Connect (SRC-110 to SRC-124)

- **SRC-110** Meltano Hub, Singer Spec. https://hub.meltano.com/singer/spec/
- **SRC-111** Meltano docs, Project concepts. https://docs.meltano.com/concepts/project/
- **SRC-112** dlt docs, Introduction. https://dlthub.com/docs/intro
- **SRC-113** dlt docs, Schema contracts. https://dlthub.com/docs/general-usage/schema-contracts
- **SRC-114** GitHub, dlt-hub/dlt README (Apache 2.0). https://github.com/dlt-hub/dlt
- **SRC-115** Estuary docs, Derivations. https://docs.estuary.dev/concepts/derivations/
- **SRC-116** Estuary Flow docs, Concepts (collections, JSON Schema, catalog sources). https://estuary.readthedocs.io/en/latest/docs/concepts.html
- **SRC-117** GitHub, estuary/flow (licence files). https://github.com/estuary/flow
- **SRC-118** Debezium docs, Architecture. https://debezium.io/documentation/reference/stable/architecture.html
- **SRC-119** Debezium docs, Outbox Event Router. https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html
- **SRC-120** Debezium docs (2.3), Sending signals to a Debezium connector. https://debezium.io/documentation/reference/2.3/configuration/signalling.html
- **SRC-121** SQLMesh docs, Concepts overview. https://sqlmesh.readthedocs.io/en/stable/concepts/overview/
- **SRC-122** Redpanda Connect docs, Enterprise Licensing; plus Bloblang "About" page (https://docs.redpanda.com/redpanda-connect/guides/bloblang/about/). https://docs.redpanda.com/redpanda-connect/get-started/licensing
- **SRC-123** Redpanda blog, Redpanda Connect. https://redpanda.com/blog/redpanda-connect
- **SRC-124** TechCrunch, Redpanda acquires Benthos (30 May 2024). https://techcrunch.com/2024/05/30/redpanda-acquires-benthos-to-expand-its-end-to-end-streaming-data-platform

### 7.13 OpenLineage and pricing commentary (SRC-125 to SRC-128)

- **SRC-125** OpenLineage docs, Integrations. https://openlineage.io/docs/next/integrations
- **SRC-126** GitHub, OpenLineage/OpenLineage. https://github.com/OpenLineage/OpenLineage
- **SRC-127** Thoughtworks Technology Radar, OpenLineage. https://www.thoughtworks.com/radar/platforms/openlineage
- **SRC-128** Hevo, Fivetran pricing guide (vendor-interested). https://hevodata.com/learn/fivetran-pricing/

### 7.14 Verification notes

- Several items were seen only in search-result summaries and not on a fetched page:
  - SRC-011 and SRC-016 (the G-Cloud minimum);
  - SRC-045 (the AWS Marketplace Talend price);
  - the Dataflow figures in SRC-099;
  - the uncited Pentaho/LEO Software acquisition claim in SRC-058.

  These are marked unverified or "snippet" in the text.
- Debezium's licence was not verified this session.
- GitHub API access was unavailable in this environment. Licences were read from GitHub repo pages through a web fetch instead.
