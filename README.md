# **Finance Agent — System Architecture, Design Reasoning, and Data Pipeline**

A **local AI-powered financial analysis assistant** built using:

* **PySide6** for the desktop interface
* **Python** for orchestration and tooling
* **LM Studio** running a local LLM (`mistralai/ministral-3-3b`)
* **Custom Python tools** for market data retrieval and chart generation

The system combines a **local language model with structured tool execution**, allowing the AI to reason about financial data while relying on deterministic Python functions to interact with the outside world.

Unlike cloud-based AI assistants, this architecture is **privacy-preserving, offline-capable, and modular**, making it suitable for both personal research and enterprise environments.



#  Design Philosophy

The system is designed around several key architectural principles.

## 1\. Separation of Concerns

Each component has a **single responsibility**.

|**Layer**|**Responsibility**|
|:-:|:-:|
|GUI|User interaction|
|Agent|Orchestration|
|LLM Client|Model communication|
|Tools|Data retrieval and computation|
|Model Server|Language model inference|

This separation ensures:

* easier debugging
* clear ownership of logic
* easier scaling and extension



## 2\. Tool-Augmented LLM Architecture

Large language models are excellent at:

* reasoning
* summarization
* natural language understanding

However, they are **not good at:**

* fetching real-time data
* running deterministic computations
* interacting with APIs

To solve this, the architecture uses **tool calling**.

The LLM becomes a **planner**, while Python tools become the **execution engine**.

```
`User Question → LLM Reasoning → Tool Request → Python Tool → Data → LLM Interpretation`
```

This hybrid architecture combines:

* **probabilistic reasoning**
* **deterministic computation**



## 3\. Security and Data Control

The system ensures:

* the **LLM never accesses the internet**
* external data access happens only through **controlled tools**
* sensitive queries remain **local to the machine**

This architecture is commonly used in **enterprise AI systems**.



#  High-Level Architecture

The system consists of five major layers.

```
`User`

`  │`

`  ▼`

`GUI (PySide6)`

`  │`

`  ▼`

`Agent Orchestrator`

`  │`

`  ▼`

`MarketInterpreter (LLM Client)`

`  │`

`  ▼`

`Python Tool Layer`

`  │`

`  ▼`

`External Data Sources`
```

The **LLM communicates only with the agent and tools**, never directly with external systems.



#  Layer-by-Layer Architecture Explanation



# 1️ GUI Layer — `finance\\\\\\\_agent.gui`

## Purpose

The GUI provides the **user interface for interacting with the Finance Agent**.

It is responsible only for **presentation and interaction**, not business logic.



## Responsibilities

* Display chat messages
* Capture user input
* Send user messages to the agent
* Render assistant responses
* Handle user interface events



## What the GUI Avoids

The GUI intentionally does **not contain**:

* AI reasoning logic
* API integrations
* market data logic
* tool execution



## Architectural Reasoning

Keeping the GUI simple ensures:

* **UI code remains maintainable**
* **business logic stays centralized**
* easier migration to other interfaces (web, CLI, API)

For example, if a web interface is added later, the agent layer can remain unchanged.



## Example Interaction

```
`User types: "PLTR"`


`GUI → agent.chat("PLTR")`
```

The GUI simply **forwards the message**.



# 2️ Agent Layer — `finance\\\\\\\_agent.agent`

## Purpose

The agent acts as the **orchestrator between the GUI and the AI system**.

It simplifies interaction with the LLM client by providing a clean interface.



## Responsibilities

* instantiate the `MarketInterpreter`
* provide a simple `chat()` interface
* route requests to the appropriate LLM method
* manage high-level orchestration



## Architectural Role

The agent functions as a **controller layer**.

Benefits:

* decouples the GUI from the AI implementation
* enables swapping LLM implementations
* allows additional middleware (logging, caching, etc.)



## Example Implementation

```
`interpreter = MarketInterpreter()`


`def chat(user\\\\\\\_message):`

`    return interpreter.chat\\\\\\\_with\\\\\\\_tools(user\\\\\\\_message)`
```



## Why This Layer Exists

Without this layer, the GUI would need to:

* understand tool-calling
* manage model loops
* handle tool responses

This would create **tight coupling between UI and AI logic**, which is bad architecture.



# 3️ LLM Client Layer — `MarketInterpreter`

Location:

```
`finance\\\\\\\_agent.llm.local\\\\\\\_agent`
```

This layer is the **core intelligence orchestration engine**.

It is responsible for interacting with **LM Studio and managing tool calls**.



## Responsibilities

* format messages for the LLM
* send HTTP requests to LM Studio
* interpret responses
* detect tool calls
* execute tools
* continue reasoning loops until a final answer is produced



## Tool Calling Loop

The key algorithm implemented here is the **LLM tool-calling loop**.

```
`1. Send user query to LLM`

`2. LLM decides if a tool is needed`

`3. If tool is requested:`

`      Execute Python function`

`4. Return result to LLM`

`5. LLM generates final response`
```

This loop continues until the LLM produces a normal message.



## Tool Registry

Tools are registered in a dictionary.

```
`self.TOOLS = \\\\{`

`    "snapshot\\\\\\\_symbol": \\\\{`

`        "args": \\\\\\\["symbol"\\\\],`

`        "func": tools.snapshot\\\\\\\_symbol,`

`    \\\\},`

`    "get\\\\\\\_ohlc": \\\\{`

`        "args": \\\\\\\["symbol", "timeframe", "limit"\\\\],`

`        "func": tools.get\\\\\\\_ohlc,`

`    \\\\},`

`    "render\\\\\\\_chart": \\\\{`

`        "args": \\\\\\\["symbol", "ohlc"\\\\],`

`        "func": tools.render\\\\\\\_chart,`

`    \\\\},`

`\\\\}`
```



## Architectural Reasoning

This registry provides three important benefits:

### 1\. Controlled Tool Access

The LLM can only call **approved tools**.



### 2\. Structured Interfaces

Arguments must match the expected schema.



### 3\. Extensibility

New tools can be added without modifying the core loop.



# 🔧 Tool Layer — `finance\\\\\\\_agent.tools`

The tool layer contains **deterministic Python functions**.

These tools interact with:

* APIs
* data sources
* charting libraries



## Why Tools Exist

LLMs cannot reliably:

* fetch live market data
* produce charts
* perform structured computations

Python tools solve these problems.



## Example Tools

### `snapshot\\\\\\\_symbol(symbol)`

Fetches a market snapshot.

Returns structured data:

```
`\\\\{`

`  "symbol": "PLTR",`

`  "price": 24.31,`

`  "change": 0.45,`

`  "volume": 45231200`

`\\\\}`
```



### `get\\\\\\\_ohlc(symbol, timeframe, limit)`

Returns OHLC candle data.

Used for:

* charting
* trend analysis
* technical indicators



### `render\\\\\\\_chart(symbol, ohlc)`

Generates a candlestick chart.

Pipeline:

```
`OHLC data`

`   ↓`

`Chart generation`

`   ↓`

`Save image to disk`

`   ↓`

`Return file path`
```



## Architectural Reasoning

Separating tools provides:

* testable code
* reusable components
* deterministic outputs

Tools can be **unit tested independently of the LLM**.



#  Model Server — LM Studio

The final layer is the **model inference server**.

LM Studio runs the local language model.

Model used:

```
`mistralai/ministral-3-3b`
```



## Responsibilities

* run LLM inference
* interpret prompts
* produce responses
* request tool calls



## Offline Operation

The model runs entirely **on the local machine**.

This means:

* no cloud calls
* no external data sharing
* predictable performance



#  Data Pipeline Overview

A key part of the system is the **data pipeline that flows between components**.



## Step 1 — User Input

```
`User enters: "PLTR"`
```



## Step 2 — GUI Event

```
`GUI → agent.chat("PLTR")`
```



## Step 3 — Agent Routing

```
`Agent → MarketInterpreter.chat\\\\\\\_with\\\\\\\_tools()`
```



## Step 4 — LLM Reasoning

The prompt is sent to the model.

The LLM determines:

* whether it can answer directly
* or needs external data



## Step 5 — Tool Invocation

Example response:

```
`tool: snapshot\\\\\\\_symbol`

`arguments: \\\\{ "symbol": "PLTR" \\\\}`
```



## Step 6 — Tool Execution

```
`Python executes snapshot\\\\\\\_symbol("PLTR")`
```

The tool fetches real market data.



## Step 7 — Tool Result Returned

The result is sent back to the LLM.



## Step 8 — Final Interpretation

The LLM interprets the data and produces a natural language response.



## Step 9 — Response Display

```
`Agent → GUI`
```

The user sees the answer.



# 🌐 Online vs Offline Behavior

## Offline Components

* LLM reasoning
* conversation handling
* summarization
* chart interpretation



## Online Components

Only the **tool layer** accesses external data.

This ensures:

* controlled data access
* auditability
* security



# 🧠 Mental Model

For developers new to the project:

|**Component**|**Analogy**|
|:-:|:-:|
|GUI|The face|
|Agent|The traffic controller|
|MarketInterpreter|The brain|
|Tools|The hands|
|LM Studio|The engine|

Important concept:

> The LLM is \\\*\\\*intelligent but blind\\\*\\\*.  
Tools give it the ability to \\\*\\\*see and act on real-world data\\\*\\\*.



# 🚀 Future Extensions

The architecture supports many future improvements:

* additional market tools
* portfolio analysis
* automated report generation
* backtesting pipelines
* real-time streaming data
* multi-model routing

Because each layer is **modular**, these additions can be made without rewriting the entire system.





 Author

Finance Agent Project

