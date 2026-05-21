# Corpus Construction Rules for `ai_system/data/raw/sample_corpus.txt`

To ensure the `sample_corpus.txt` serves as a high-quality foundation for the `myTinyGPT` transformer, all content added to this file must adhere to the following professional standards.

## 1. Data Integrity and Formatting

- **Encoding:** File MUST be strictly UTF-8 encoded to prevent tokenization errors.
- **Normalization:** Normalize all whitespace to single spaces (except line breaks). Avoid tabs and non-breaking spaces.
- **Line Structure:** Each line should ideally represent a complete logical thought or code block. Avoid breaking sentences across lines arbitrarily.
- **No Metadata:** The file should contain pure text data only. No headers, footers, JSON structures, or markdown fence labels unless the corpus loader explicitly expects them.
- **Pure Content:** There should be no embedded dataset labels, system prompts, or training metadata inside the text.

## 2. Content Quality Standards

- **Technical Accuracy:** All code samples MUST be syntactically correct, idiomatic, and preferably runnable with minimal adaptation. Avoid pseudocode.
- **Language Scope:** Focus on JavaScript/Node.js, TypeScript, and relevant web technologies.
- **Educational Value:** Prefer the "Explain -> Example -> Best Practice" pattern for text segments.
- **Diversity:** Ensure a balanced distribution between:
  - Language features (closures, async/await, prototypes)
  - Browser APIs (DOM, fetch, storage)
  - Backend/System (Node.js buffers, streams, events, file system)
  - Architecture and tooling (patterns, testing, security, deployment)
- **Practicality:** Favor real-world engineering constraints such as error handling, performance optimization, memory management, and security.

## 3. Training Format and Pipeline Alignment

- **Corpus loader compatibility:** Confirm the generated corpus format matches the actual training pipeline used by `ai_system/app/training/dataset.py` or the fine-tuning script.
- **Raw text training:** The current dataset loader reads plain text and tokenizes it directly. If using structured instruction-response data, ensure the raw file preserves that format without introducing unsupported tokens.
- **No false expectations:** Do not require `USER:` / `ASSISTANT:` or fenced sections unless the data will be preprocessed into the trainer’s accepted format.

## 4. Training Optimization (SentencePiece)

- **Vocabulary Coverage:** Include a wide range of standard identifiers (`variables`, `let / const / var`, `scope`, `hoisting`, `closures`, `prototypes`, `prototype chain`, `classes`, `inheritance`, `modules`, `CommonJS`, `ES Modules`, `destructuring`, `spread operator`, `rest parameters`, `template literals`, `optional chaining`, `nullish coalescing`, `arrow functions`, `higher-order functions`, `callbacks`, `recursion`, `generators`, `iterators`, `async iteration`, `promises`, `async/await`, `event loop`, `microtasks`, `macrotasks`, `memory management`, `garbage collection`, `type coercion`, `equality operators`, `symbols`, `BigInt`, `strict mode`, `functional programming`, `immutability`, `currying`, `memoization`, `debouncing`, `throttling`, `arrays`, `array methods`, `map`, `filter`, `reduce`, `find`, `some`, `every`, `flat`, `flatMap`, `sorting`, `searching`, `linked lists`, `queues`, `stacks`, `trees`, `graphs`, `sets`, `maps`, `weakmaps`, `weaksets`, `hash maps`, `priority queues`, `object manipulation`, `deep clone`, `shallow clone`, `object freezing`, `object sealing`, `JSON parsing`, `JSON serialization`, `circular references`, `schema validation`, `DOM manipulation`, `querySelector`, `event listeners`, `event delegation`, `forms`, `drag and drop`, `clipboard API`, `history API`, `location API`, `URLSearchParams`, `fetch API`, `XMLHttpRequest`, `localStorage`, `sessionStorage`, `IndexedDB`, `cookies`, `Web Workers`, `Service Workers`, `notifications`, `geolocation`, `intersection observer`, `mutation observer`, `resize observer`, `canvas`, `WebGL`, `WebGPU`, `audio API`, `media devices`, `camera access`, `microphone access`, `fullscreen API`, `file API`, `streams API`, `REST APIs`, `GraphQL`, `WebSockets`, `Socket.IO`, `Server-Sent Events`, `HTTP methods`, `headers`, `authentication`, `JWT`, `OAuth`, `cookies vs tokens`, `CORS`, `rate limiting`, `retries`, `exponential backoff`, `request cancellation`, `streaming responses`, `multipart uploads`, `React basics`, `JSX`, `components`, `props`, `state`, `hooks`, `useState`, `useEffect`, `useMemo`, `useCallback`, `useReducer`, `useRef`, `custom hooks`, `context API`, `React Router`, `lazy loading`, `suspense`, `concurrent rendering`, `hydration`, `server components`, `form handling`, `controlled inputs`, `uncontrolled inputs`, `React performance`, `React debugging`, `React testing`, `React architecture`, `state management`, `Redux`, `Zustand`, `Recoil`, `MobX`, `React Query`, `TanStack Query`, `Next.js`, `Remix`, `Vite`, `SSR`, `CSR`, `SSG`, `ISR`, `Node.js runtime`, `event emitter`, `buffers`, `streams`, `child processes`, `worker threads`, `cluster mode`, `file system APIs`, `path module`, `process module`, `environment variables`, `timers`, `HTTP server`, `HTTPS server`, `TCP sockets`, `UDP sockets`, `crypto module`, `zlib`, `readline`, `REPL`, `CLI tools`, `daemon processes`, `Express.js`, `Fastify`, `Koa`, `NestJS`, `middleware`, `routing`, `validation`, `authentication`, `authorization`, `sessions`, `cookies`, `logging`, `API design`, `REST conventions`, `GraphQL resolvers`, `OpenAPI`, `Swagger`, `microservices`, `WebSocket servers`, `background jobs`, `queues`, `cron jobs`, `caching`, `MongoDB`, `PostgreSQL`, `MySQL`, `SQLite`, `Redis`, `Prisma`, `Sequelize`, `Mongoose`, `query optimization`, `indexing`, `transactions`, `migrations`, `ORM patterns`, `typing`, `interfaces`, `generics`, `utility types`, `enums`, `discriminated unions`, `type guards`, `declaration files`, `tsconfig`, `strict typing`, `advanced types`, `npm`, `yarn`, `pnpm`, `package.json`, `lock files`, `semantic versioning`, `webpack`, `vite`, `rollup`, `babel`, `swc`, `esbuild`, `eslint`, `prettier`, `husky`, `lint-staged`, `nodemon`, `ts-node`, `unit testing`, `integration testing`, `end-to-end testing`, `Jest`, `Vitest`, `Mocha`, `Cypress`, `Playwright`, `mocking`, `snapshots`, `test coverage`, `async testing`, `stack traces`, `source maps`, `memory leaks`, `race conditions`, `infinite loops`, `async bugs`, `promise debugging`, `React render loops`, `Node.js profiling`, `Chrome DevTools`, `network debugging`, `performance tracing`, `heap snapshots`, `code splitting`, `lazy loading`, `memoization`, `virtualization`, `caching`, `compression`, `CDN usage`, `bundle analysis`, `tree shaking`, `render optimization`, `database optimization`, `event optimization`, `stream processing`, `XSS`, `CSRF`, `SQL injection`, `command injection`, `SSRF`, `sanitization`, `input validation`, `password hashing`, `rate limiting`, `secure cookies`, `CSP headers`, `JWT security`, `secrets management`, `Docker`, `Docker Compose`, `CI/CD`, `GitHub Actions`, `PM2`, `Nginx`, `reverse proxies`, `Ubuntu deployment`, `environment configs`, `SSL certificates`, `domain setup`, `monitoring`, `logging`, `scaling`, `load balancing`, `monorepos`, `API integrations`, `payment processing`, `Stripe`, `Firebase`, `Supabase`, `AWS SDK`, `file uploads`, `image processing`, `authentication systems`, `chat applications`, `multiplayer systems`, `collaborative editing`, `dashboards`, `admin panels`, `CMS systems`, `TensorFlow.js`, `ONNX runtime`, `OpenAI APIs`, `embeddings`, `vector databases`, `RAG systems`, `streaming AI responses`, `websocket AI chat`, `AI agents`, `local LLM tooling`, `React Native`, `Expo`, `Capacitor`, `Electron`, `Tauri`, `PWA development`, `binary data`, `protobuf`, `WebRTC`, `peer-to-peer networking`, `browser rendering`, `hydration mismatches`, `accessibility`, `i18n`, `localization`, `animation`, `game loops`, `Three.js`, `Babylon.js`, `MIDI APIs`, `serial APIs`, `Bluetooth APIs`, `IoT integration`), punctuation, and common API names.
- **Context Length:** Aim for average sentence/code block lengths between 50 and 150 tokens to help the model learn mid-range dependencies inside the 256-token window.
- **Noise Control:** Remove excessive boilerplate, long comment blocks, and non-ASCII sequences that do not contribute to learning JavaScript structure.
- **Balance:** Avoid very long monologues; chunk long explanations into smaller, coherent sections.

## 5. Validation, QA, and Data Hygiene

- **Holdout data:** Reserve a separate validation/held-out set whenever possible, or keep a distinct file for model evaluation.
- **Verify formatting:** After generation, validate the corpus for unicode issues, stray metadata, malformed code fences, and repeated boilerplate.
- **Uniqueness:** Ensure examples are not duplicated verbatim across the corpus.
- **No prompt leakage:** Do not include hidden system prompts, training labels, or internal instructions in production corpus data.

## 6. Corpus Structuring Rules

- **Logical Grouping:** Sequence related topics so the model can learn transitions (for example, explain promises and then show async/await refactorings).
- **Topic variety:** Avoid over-weighting one category. Mix debugging, refactoring, architecture, and API usage.
- **Entry uniqueness:** Similar scenarios should vary variable names, error cases, environment assumptions, or implementation details. Each variant should have genuinely distinct code/examples or the corpus should avoid repeating the same template across multiple entries.
- **No filler:** Avoid repetitive generic examples such as "Hello World" and meaningless boilerplate.

## 7. Formatting & Structure Requirements

- **Instruction style:** If the dataset is intended as an instruction corpus, use explicit `USER:` / `ASSISTANT:` or `INSTRUCTION`/`RESPONSE` structure consistently.
- **Code Blocks:** All code examples should use fenced `js ... ` blocks when the corpus is intended to preserve code structure explicitly.
- **Dialogue clarity:** When using QA format, keep the prompt concise and the response focused, explanatory, and action-oriented.
- **Follow-up examples:** If including multi-turn examples, keep the follow-up on-topic and reference prior context naturally.

## 8. Security and Safety

- **Secure defaults:** Prefer secure implementations and avoid encouraging insecure practices unless the example is explicitly labeled as an anti-pattern.
- **No exploit recipes:** Do not include examples that teach bypassing authentication, disabling security controls, or exploiting vulnerabilities.
- **Safe error handling:** Encourage proper validation, sanitization, and defensive programming.

## 9. Provenance and Licensing

- **Source attribution:** Use only content that is licensed for reuse or authored directly. Do not mix proprietary, unlicensed, or copyrighted source text without permission.
- **Clear provenance:** Document the origin of large corpus contributions when possible.
- **Consistent quality:** Do not copy large swaths of third-party text verbatim unless licenses allow it.

## 10. Problem Domain & Coverage

- **Problem patterns:** Cover common JS/Node patterns and failure modes such as async race conditions, memory leaks, scope confusion, event loop blocking, prototype chain issues, and dependency management.
- **Language breadth:** Require the corpus to span a wide range of JavaScript topics, including core language features, runtime behavior, browser APIs, Node.js systems, React/SSR tooling, backend services, testing, deployment, security, performance, and modern package/toolchain ecosystems.
- **Debugging and refactoring:** Include examples that show systematic debugging, stack trace interpretation, and code improvement.
- **API usage:** Demonstrate real-world Node.js and Browser API usage with best-practice patterns.
- **Balanced coverage:** Make sure the corpus is not biased toward a single framework or library absent a clear project focus.
