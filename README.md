
# print("Hello Pythonic+ !")

### Pythonic+ (Also known as PPlus) is a Python+ Library that adds various little things to make development just a bit easier and faster.

It adds various new functions like easier Bit storing (idk why one would need this but anyway), and a bit easier Yaml, Toml, Xml (and json, just done for the vibes) parsing.

---

## The Bits and Bobs (Data Section)

The data layer is built around the idea of zero friction. There is no need to learn multiple distinct libraries to handle different file configurations.

### 1. Unified Data Parsing

Instead of importing separate modules for json, toml, yaml, and xml, PPlus routes everything through a single entry point.

* **The Workflow:** Point PPlus at a target file. The internal engine detects the formatting and returns the structured data instantly.
* **Conversion:** Load a JSON file and save it as a TOML file in two operations. This format-agnostic approach is handled natively by the UniversalData module.

### 2. The BitStore Managed Memory

Standard Python lists carry heavy overhead. When an application strictly needs to track binary states (such as hardware flags, network protocols, or logic gates), BitStore provides a highly optimized alternative.

* **Manual Control:** Flip, set, or reset individual bits directly by their index.
* **Efficiency:** Data is stored in a minimal format that respects the binary nature of the underlying hardware, drastically reducing memory footprint during large-scale operations.

---

## System Architecture and Execution

The system engines handle the heavy lifting of execution and timing, bridging high-level scripting with low-level predictability.

### 1. The HyperLoop (Consistent Timing)

Standard loops execute as rapidly as the CPU allows, which can cause inconsistent application behavior and stuttering across different machines.

* **The Delta-Time Strategy:** HyperLoop constantly calculates the exact time between execution frames. It ensures that internal logic runs at a stable, predetermined frequency, regardless of the system's processing load.
* **Usage:** Ideal for tasks requiring steady, repeated execution, such as data polling, state management, or UI rendering cycles.

### 2. The Transformer (Deployment Packaging)

Distributing Python applications traditionally requires shipping raw source code. The Transformer provides a secure, compiled alternative for production deployment.

* **The Build Process:** The build system takes standard Python scripts and packs them alongside any native assemblies into a standalone `.pplus` file.
* **Binary Streaming:** This generated file operates as a raw, length-prefixed binary stream. It obscures the source logic and significantly optimizes load times for the internal PPlus runtime environment.

---

## The Command Line Interface (CLI)

PPlus is managed directly through the terminal. This keeps the workspace clean and strictly adheres to professional deployment standards.

| Command | Action |
| --- | --- |
| `pplus repl` | Opens the interactive shell for testing Python and native snippets in real-time. |
| `pplus watch [file]` | Monitors a target script and automatically re-executes the environment upon detecting saved changes. |
| `pplus build [file]` | Transforms a script into a standalone `.pplus` binary format. |
| `pplus run [file]` | Executes a compiled `.pplus` bundle using the isolated execution runtime. |

---

## Quick Setup

1. Install the framework via pip: `pip install pplus`
2. Initialize a project directory and create the core entry script.
3. Deploy the application using the build command to generate the secure distribution file.

## License

PPlus is released under the MIT License.
