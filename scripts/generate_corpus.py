from pathlib import Path
import textwrap

base_templates = [
    {
        'prompt': 'How do I avoid scope issues between let, const, and var?',
        'answer': 'Use let and const for block scope, avoid var in modern code, and declare variables close to their usage.',
        'code': textwrap.dedent('''
            function buildList(items) {
              let list = []
              for (const item of items) {
                list.push(item)
              }
              return list
            }
        ''')
    },
    {
        'prompt': 'How does hoisting affect var and function declarations?',
        'answer': 'Function declarations hoist the body, var declarations hoist the variable name, and let/const are block-scoped and not initialized until execution reaches them.',
        'code': textwrap.dedent('''
            console.log(fn())
            function fn() {
              return 'hoisted'
            }
        ''')
    },
    {
        'prompt': 'How do closures preserve private state in JavaScript?',
        'answer': 'Closures capture lexical scope so inner functions can access variables defined in outer functions even after they return.',
        'code': textwrap.dedent('''
            function counter() {
              let count = 0
              return () => ++count
            }
            const next = counter()
            console.log(next())
        ''')
    },
    {
        'prompt': 'How does prototype chain inheritance work in JavaScript?',
        'answer': 'Objects inherit properties through the prototype chain, so methods defined on the prototype are shared by instances.',
        'code': textwrap.dedent('''
            function Animal(name) {
              this.name = name
            }
            Animal.prototype.speak = function() {
              return `${this.name} makes a noise`
            }
        ''')
    },
    {
        'prompt': 'How do I implement class inheritance with extends?',
        'answer': 'Use class extends and call super() in the subclass constructor to inherit parent behavior.',
        'code': textwrap.dedent('''
            class Vehicle {
              constructor(model) {
                this.model = model
              }
            }
            class Car extends Vehicle {
              constructor(model, doors) {
                super(model)
                this.doors = doors
              }
            }
        ''')
    },
    {
        'prompt': 'How do CommonJS exports work in Node.js?',
        'answer': 'Assign values to module.exports and require() them from other files, keeping module boundaries explicit.',
        'code': textwrap.dedent('''
            const fs = require('fs')
            module.exports = function readJson(path) {
              return JSON.parse(fs.readFileSync(path, 'utf8'))
            }
        ''')
    },
    {
        'prompt': 'How do ES modules import and export values?',
        'answer': 'Use export/import syntax to share values between modules and enable tree shaking in modern bundlers.',
        'code': textwrap.dedent('''
            export function parseData(json) {
              return JSON.parse(json)
            }
            import { parseData } from './utils.js'
        ''')
    },
    {
        'prompt': 'How do I destructure nested objects safely?',
        'answer': 'Use nested destructuring with default values to avoid crashes when properties are missing.',
        'code': textwrap.dedent('''
            const { user = {} } = payload
            const { name = 'Guest', email = '' } = user
            console.log(name, email)
        ''')
    },
    {
        'prompt': 'How can I use the spread operator to merge arrays and objects?',
        'answer': 'Use ... to copy or merge arrays and objects without mutating the originals.',
        'code': textwrap.dedent('''
            const defaults = { theme: 'light' }
            const config = { ...defaults, theme: 'dark' }
            const items = [...baseItems, 'extra']
        ''')
    },
    {
        'prompt': 'How do rest parameters simplify function signatures?',
        'answer': 'Rest parameters gather extra arguments into an array, making variadic functions easier to write.',
        'code': textwrap.dedent('''
            function sum(...values) {
              return values.reduce((total, value) => total + value, 0)
            }
            console.log(sum(1, 2, 3))
        ''')
    },
    {
        'prompt': 'How do template literals improve multiline strings and interpolation?',
        'answer': 'Template literals let you embed expressions and write multiline strings without concatenation.',
        'code': textwrap.dedent('''
            const user = { name: 'Alex', items: 3 }
            const message = `User ${user.name} has ${user.items} items.`
            console.log(message)
        ''')
    },
    {
        'prompt': 'How does optional chaining avoid runtime errors?',
        'answer': 'Optional chaining stops property access if any part of the chain is undefined, preventing TypeError exceptions.',
        'code': textwrap.dedent('''
            const city = user?.address?.city ?? 'unknown'
            console.log(city)
        ''')
    },
    {
        'prompt': 'How does nullish coalescing differ from ||?',
        'answer': 'Use ?? to preserve falsey values like 0 and '' while only substituting when a value is null or undefined.',
        'code': textwrap.dedent('''
            const count = userCount ?? 0
            console.log('count', count)
        ''')
    },
    {
        'prompt': 'How do arrow functions differ from regular functions?',
        'answer': 'Arrow functions inherit this from their parent scope and are more concise for small callbacks.',
        'code': textwrap.dedent('''
            const numbers = [1, 2, 3]
            const doubled = numbers.map(n => n * 2)
            console.log(doubled)
        ''')
    },
    {
        'prompt': 'How do higher-order functions help with reusable logic?',
        'answer': 'Higher-order functions accept or return other functions, enabling composition and abstraction.',
        'code': textwrap.dedent('''
            function withLogging(fn) {
              return (...args) => {
                console.log('calling', fn.name)
                return fn(...args)
              }
            }
        ''')
    },
    {
        'prompt': 'How do I handle async callbacks that use the error-first pattern?',
        'answer': 'Check the error argument first and only process the result if there is no error.',
        'code': textwrap.dedent('''
            fs.readFile(path, 'utf8', (err, data) => {
              if (err) return console.error(err)
              console.log(data)
            })
        ''')
    },
    {
        'prompt': 'How can recursion traverse a tree structure?',
        'answer': 'Use a recursive function that visits the current node and then recurses into each child.',
        'code': textwrap.dedent('''
            function walk(node) {
              console.log(node.value)
              node.children?.forEach(walk)
            }
        ''')
    },
    {
        'prompt': 'How do generator functions yield lazy sequences?',
        'answer': 'Generator functions yield values one at a time and pause between iterations.',
        'code': textwrap.dedent('''
            function* range(n) {
              for (let i = 0; i < n; i++) {
                yield i
              }
            }
            for (const value of range(3)) {
              console.log(value)
            }
        ''')
    },
    {
        'prompt': 'How do async iterators process stream chunks?',
        'answer': 'Use for await...of to consume asynchronous data sources sequentially.',
        'code': textwrap.dedent('''
            async function process(stream) {
              for await (const chunk of stream) {
                console.log(chunk.toString())
              }
            }
        ''')
    },
    {
        'prompt': 'How should I chain promises and handle errors?',
        'answer': 'Attach catch at the end of the chain and return values explicitly to maintain flow.',
        'code': textwrap.dedent('''
            fetch(url)
              .then(res => res.json())
              .then(data => data.items)
              .catch(err => console.error('fetch failed', err))
        ''')
    },
    {
        'prompt': 'How do I write async/await code with error handling?',
        'answer': 'Wrap await calls in try/catch and avoid swallowing exceptions silently.',
        'code': textwrap.dedent('''
            async function load() {
              try {
                const res = await fetch('/api/data')
                return await res.json()
              } catch (error) {
                console.error('load failed', error)
              }
            }
        ''')
    },
    {
        'prompt': 'How do microtasks and macrotasks affect execution order?',
        'answer': 'Microtasks run before the next repaint, while macrotasks run after the current JavaScript stack clears.',
        'code': textwrap.dedent('''
            Promise.resolve().then(() => console.log('microtask'))
            setTimeout(() => console.log('macrotask'), 0)
            console.log('sync')
        ''')
    },
    {
        'prompt': 'How can I avoid memory leaks from event listeners?',
        'answer': 'Remove event listeners when the element is no longer needed to avoid retained references.',
        'code': textwrap.dedent('''
            const handler = () => console.log('clicked')
            button.addEventListener('click', handler)
            button.removeEventListener('click', handler)
        ''')
    },
    {
        'prompt': 'How does WeakMap help with garbage collection?',
        'answer': 'WeakMap keys are weakly referenced so they can be collected when there are no other references.',
        'code': textwrap.dedent('''
            const cache = new WeakMap()
            const obj = {}
            cache.set(obj, 'value')
        ''')
    },
    {
        'prompt': 'How do strict equality and type coercion differ?',
        'answer': '=== compares both type and value, while == performs type coercion before comparison.',
        'code': textwrap.dedent('''
            console.log(0 === '0')
            console.log(0 == '0')
        ''')
    },
    {
        'prompt': 'Why use Symbol for object keys?',
        'answer': 'Symbols create unique keys that avoid accidental collisions with string properties.',
        'code': textwrap.dedent('''
            const id = Symbol('id')
            const obj = { [id]: 1 }
            console.log(obj[id])
        ''')
    },
    {
        'prompt': 'How do you perform arithmetic with BigInt?',
        'answer': 'Use BigInt literals or BigInt() to handle values outside the safe integer range.',
        'code': textwrap.dedent('''
            const big = 9007199254740991n
            console.log(big + 1n)
        ''')
    },
    {
        'prompt': 'How does strict mode help catch bugs?',
        'answer': 'Strict mode prevents silent errors and disables problematic language features like implicit globals.',
        'code': textwrap.dedent('''
            'use strict'
            function foo() {
              // undeclared = 1 would throw here
            }
            foo()
        ''')
    },
    {
        'prompt': 'How can functional programming improve immutability?',
        'answer': 'Use pure functions and immutable operations to avoid shared mutable state.',
        'code': textwrap.dedent('''
            const newList = list.map(item => ({ ...item, selected: false }))
        ''')
    },
    {
        'prompt': 'How do you create curried functions?',
        'answer': 'Return nested functions so each call receives one argument and returns a new function.',
        'code': textwrap.dedent('''
            function add(x) {
              return function(y) {
                return x + y
              }
            }
            console.log(add(2)(3))
        ''')
    },
    {
        'prompt': 'How does memoization speed up repeated calculations?',
        'answer': 'Cache function results so repeated calls with the same arguments reuse the computed value.',
        'code': textwrap.dedent('''
            const cache = new Map()
            function fib(n) {
              if (cache.has(n)) return cache.get(n)
              const value = n < 2 ? n : fib(n - 1) + fib(n - 2)
              cache.set(n, value)
              return value
            }
        ''')
    },
    {
        'prompt': 'How do I debounce a frequent input event?',
        'answer': 'Delay the handler until the user stops typing to reduce unnecessary work.',
        'code': textwrap.dedent('''
            let timer
            input.addEventListener('input', () => {
              clearTimeout(timer)
              timer = setTimeout(() => search(input.value), 300)
            })
        ''')
    },
    {
        'prompt': 'How do I throttle a scroll handler?',
        'answer': 'Limit how often the handler runs to avoid overwhelming the browser during scroll events.',
        'code': textwrap.dedent('''
            let last = 0
            window.addEventListener('scroll', () => {
              const now = Date.now()
              if (now - last > 200) {
                last = now
                updateScroll()
              }
            })
        ''')
    },
    {
        'prompt': 'How do map, filter, and reduce differ?',
        'answer': 'map transforms items, filter selects items, and reduce folds items into a single result.',
        'code': textwrap.dedent('''
            const nums = [1, 2, 3]
            const doubled = nums.map(n => n * 2)
            const evens = nums.filter(n => n % 2 === 0)
            const sum = nums.reduce((acc, n) => acc + n, 0)
        ''')
    },
    {
        'prompt': 'How do find, some, and every help array searches?',
        'answer': 'find returns the first match, some checks for any match, and every verifies all items match.',
        'code': textwrap.dedent('''
            const users = [{ active: false }, { active: true }]
            console.log(users.find(u => u.active))
            console.log(users.some(u => u.active))
            console.log(users.every(u => u.active))
        ''')
    },
    {
        'prompt': 'How can flat and flatMap simplify nested arrays?',
        'answer': 'Use flat to flatten arrays and flatMap to map and flatten in a single step.',
        'code': textwrap.dedent('''
            const nested = [[1, 2], [3, 4]]
            console.log(nested.flat())
            console.log(nested.flatMap(x => x.map(n => n * 2)))
        ''')
    },
    {
        'prompt': 'How do you build a simple linked list in JavaScript?',
        'answer': 'Use nodes with next pointers and update references when inserting or removing elements.',
        'code': textwrap.dedent('''
            function ListNode(value) {
              this.value = value
              this.next = null
            }
            const head = new ListNode(1)
            head.next = new ListNode(2)
        ''')
    },
    {
        'prompt': 'How do I implement a queue with push and shift?',
        'answer': 'Use an array and add items to the end while removing them from the front.',
        'code': textwrap.dedent('''
            const queue = []
            queue.push('a')
            const item = queue.shift()
            console.log(item)
        ''')
    },
    {
        'prompt': 'How do Set and Map improve lookups over plain objects?',
        'answer': 'Set and Map support arbitrary key types and preserve insertion order.',
        'code': textwrap.dedent('''
            const set = new Set([1, 2, 3])
            const map = new Map([['a', 1]])
            console.log(set.has(2), map.get('a'))
        ''')
    },
    {
        'prompt': 'Why use WeakMap for caching objects?',
        'answer': 'WeakMap entries do not prevent garbage collection of keys that are only referenced there.',
        'code': textwrap.dedent('''
            const cache = new WeakMap()
            const obj = { id: 1 }
            cache.set(obj, 'cached')
        ''')
    },
    {
        'prompt': 'How do I deep clone objects without sharing references?',
        'answer': 'Use structured cloning or JSON methods for plain objects, and avoid copying by reference.',
        'code': textwrap.dedent('''
            const clone = JSON.parse(JSON.stringify(original))
            console.log(clone)
        ''')
    },
    {
        'prompt': 'How do I freeze an object to prevent mutation?',
        'answer': 'Object.freeze makes the top-level object immutable, but nested objects still need their own freeze calls.',
        'code': textwrap.dedent('''
            const config = Object.freeze({ mode: 'read-only' })
            console.log(config.mode)
        ''')
    },
    {
        'prompt': 'How do I validate JSON payloads safely?',
        'answer': 'Parse JSON inside try/catch and verify the expected shape before using the data.',
        'code': textwrap.dedent('''
            try {
              const body = JSON.parse(req.body)
              if (typeof body.name !== 'string') throw new Error('Invalid body')
            } catch (err) {
              res.status(400).send('Invalid JSON')
            }
        ''')
    },
    {
        'prompt': 'How do I use URLSearchParams for query parameters?',
        'answer': 'Build query strings with URLSearchParams instead of manual concatenation to avoid encoding bugs.',
        'code': textwrap.dedent('''
            const params = new URLSearchParams({ q: 'search', page: 1 })
            const url = `/api?${params}`
        ''')
    },
    {
        'prompt': 'How can I delegate form submit handling to a parent element?',
        'answer': 'Use event delegation to handle multiple controls with a single listener.',
        'code': textwrap.dedent('''
            form.addEventListener('submit', event => {
              event.preventDefault()
              if (event.target.matches('input')) {
                console.log('form submitted')
              }
            })
        ''')
    },
    {
        'prompt': 'How do I cache user state in localStorage?',
        'answer': 'Serialize state to JSON and restore it on page load to persist user preferences.',
        'code': textwrap.dedent('''
            localStorage.setItem('theme', 'dark')
            console.log(localStorage.getItem('theme'))
        ''')
    },
    {
        'prompt': 'How do I store records in IndexedDB?',
        'answer': 'Open a database transaction and add records through an object store.',
        'code': textwrap.dedent('''
            const request = indexedDB.open('app', 1)
            request.onsuccess = () => {
              const db = request.result
              const tx = db.transaction('store', 'readwrite')
            }
        ''')
    },
    {
        'prompt': 'How do Web Workers send messages back to the main thread?',
        'answer': 'Post messages from the worker and listen for them on the main thread.',
        'code': textwrap.dedent('''
            worker.onmessage = event => console.log(event.data)
            worker.postMessage({ task: 'compute' })
        ''')
    },
    {
        'prompt': 'How do Service Workers handle fetch events for caching?',
        'answer': 'Intercept fetch events and return cached responses when available.',
        'code': textwrap.dedent('''
            self.addEventListener('fetch', event => {
              event.respondWith(caches.match(event.request))
            })
        ''')
    },
    {
        'prompt': 'How do I connect to a WebSocket server from the browser?',
        'answer': 'Create a WebSocket and listen for open, message, and close events.',
        'code': textwrap.dedent('''
            const socket = new WebSocket('wss://example.com')
            socket.onmessage = event => console.log(event.data)
        ''')
    },
    {
        'prompt': 'How do I add request logging middleware in Express?',
        'answer': 'Add middleware early to log method, path, and request metadata for all incoming requests.',
        'code': textwrap.dedent('''
            app.use((req, res, next) => {
              console.log(`${req.method} ${req.url}`)
              next()
            })
        ''')
    },
    {
        'prompt': 'How do I secure a JWT cookie in Express?',
        'answer': 'Set HttpOnly, Secure, and SameSite attributes when sending JWT cookies.',
        'code': textwrap.dedent('''
            res.cookie('token', jwt, { httpOnly: true, secure: true, sameSite: 'lax' })
        ''')
    },
    {
        'prompt': 'How do I handle CORS preflight requests correctly?',
        'answer': 'Respond to OPTIONS requests with the appropriate Access-Control headers before allowing the main request.',
        'code': textwrap.dedent('''
            app.options('/api', (req, res) => {
              res.set('Access-Control-Allow-Origin', '*')
              res.sendStatus(204)
            })
        ''')
    },
    {
        'prompt': 'How do I apply simple rate limiting to an API route?',
        'answer': 'Track request counts per client and reject requests that exceed a threshold in a time window.',
        'code': textwrap.dedent('''
            const requests = new Map()
            app.use((req, res, next) => {
              const count = requests.get(req.ip) || 0
              if (count > 100) return res.status(429).send('Too many requests')
              requests.set(req.ip, count + 1)
              next()
            })
        ''')
    },
    {
        'prompt': 'How do I parse multipart uploads in Express?',
        'answer': 'Use a streaming parser or middleware to handle file uploads without buffering the entire payload.',
        'code': textwrap.dedent('''
            const multer = require('multer')
            const upload = multer({ dest: '/tmp' })
            app.post('/upload', upload.single('file'), (req, res) => {
              res.send('uploaded')
            })
        ''')
    },
    {
        'prompt': 'How do I manage form state with React useState?',
        'answer': 'Store field values in state and update them via controlled inputs.',
        'code': textwrap.dedent('''
            const [value, setValue] = useState('')
            return <input value={value} onChange={e => setValue(e.target.value)} />
        ''')
    },
    {
        'prompt': 'How do I clean up side effects in React useEffect?',
        'answer': 'Return a cleanup function from useEffect to remove listeners or cancel async work.',
        'code': textwrap.dedent('''
            useEffect(() => {
              window.addEventListener('resize', handleResize)
              return () => window.removeEventListener('resize', handleResize)
            }, [])
        ''')
    },
    {
        'prompt': 'How can I use useRef for DOM access in React?',
        'answer': 'Attach a ref to an element and read the DOM node from ref.current when needed.',
        'code': textwrap.dedent('''
            const inputRef = useRef(null)
            useEffect(() => {
              inputRef.current?.focus()
            }, [])
        ''')
    },
    {
        'prompt': 'How do I provide global state with React Context?',
        'answer': 'Create a Context provider and consume values with useContext inside nested components.',
        'code': textwrap.dedent('''
            const ThemeContext = React.createContext('light')
            function App() {
              return <ThemeContext.Provider value='dark' />
            }
        ''')
    },
    {
        'prompt': 'How do I lazy load a React component?',
        'answer': 'Use React.lazy and Suspense to load components only when they are rendered.',
        'code': textwrap.dedent('''
            const LazyComponent = React.lazy(() => import('./LazyComponent'))
            return <Suspense fallback={<div>Loading...</div>}><LazyComponent /></Suspense>
        ''')
    },
    {
        'prompt': 'How do I fetch data for server-side rendering?',
        'answer': 'Fetch data in the server context before rendering and pass it to the page.',
        'code': textwrap.dedent('''
            export async function getServerSideProps() {
              const res = await fetch('https://api.example.com/data')
              return { props: { data: await res.json() } }
            }
        ''')
    },
    {
        'prompt': 'How do I write an async Jest test?',
        'answer': 'Use async/await in the test function and assert the resolved value or thrown error.',
        'code': textwrap.dedent('''
            test('loads data', async () => {
              const data = await fetchData()
              expect(data).toHaveProperty('id')
            })
        ''')
    },
    {
        'prompt': 'How do I write a TypeScript type guard?',
        'answer': 'Return a boolean and use the is keyword to narrow types in conditional branches.',
        'code': textwrap.dedent('''
            function isString(value) {
              return typeof value === 'string'
            }
        ''')
    },
    {
        'prompt': 'How do I spawn a child process in Node.js?',
        'answer': 'Use child_process.spawn and listen for stdout, stderr, and exit events.',
        'code': textwrap.dedent('''
            const { spawn } = require('child_process')
            const proc = spawn('ls', ['-la'])
            proc.stdout.on('data', console.log)
        ''')
    },
    {
        'prompt': 'How do worker threads help with CPU-bound tasks?',
        'answer': 'Offload intensive computation to a worker thread so the main event loop stays responsive.',
        'code': textwrap.dedent('''
            const { Worker } = require('worker_threads')
            new Worker('./worker.js').postMessage({ task: 'compress' })
        ''')
    },
    {
        'prompt': 'How can I build a CLI with readline?',
        'answer': 'Use readline.createInterface to prompt users and read input from stdin.',
        'code': textwrap.dedent('''
            const readline = require('readline')
            const rl = readline.createInterface({ input: process.stdin, output: process.stdout })
            rl.question('Name? ', answer => { console.log(answer); rl.close() })
        ''')
    },
    {
        'prompt': 'How do I validate request bodies with Zod in Express?',
        'answer': 'Parse the request body with a Zod schema and return a 400 error on failure.',
        'code': textwrap.dedent('''
            const schema = z.object({ name: z.string() })
            const result = schema.safeParse(req.body)
            if (!result.success) return res.status(400).json(result.error)
        ''')
    },
    {
        'prompt': 'How do I cache results in Redis?',
        'answer': 'Store computed values in Redis and return the cached value if it exists.',
        'code': textwrap.dedent('''
            await redis.set('user:1', JSON.stringify(user))
            const cached = await redis.get('user:1')
        ''')
    },
    {
        'prompt': 'How do I run a Prisma transaction?',
        'answer': 'Use prisma.$transaction to execute multiple queries atomically.',
        'code': textwrap.dedent('''
            await prisma.$transaction([
              prisma.user.create({ data: user }),
              prisma.post.create({ data: post }),
            ])
        ''')
    },
    {
        'prompt': 'How do I add a developer script to package.json?',
        'answer': 'Add a script entry that runs your development command, like nodemon or vite.',
        'code': textwrap.dedent('''
            // package.json
            {
              "scripts": {
                "dev": "vite"
              }
            }
        ''')
    },
    {
        'prompt': 'How do I configure ESLint and Prettier together?',
        'answer': 'Use eslint-config-prettier to avoid formatting conflicts between ESLint and Prettier.',
        'code': textwrap.dedent('''
            module.exports = {
              extends: ['eslint:recommended', 'plugin:prettier/recommended'],
            }
        ''')
    },
    {
        'prompt': 'How do I mock network requests in tests?',
        'answer': 'Use test doubles or fetch mocks so tests do not depend on real network responses.',
        'code': textwrap.dedent('''
            global.fetch = jest.fn(() => Promise.resolve({ json: () => ({}) }))
        ''')
    },
    {
        'prompt': 'How do source maps help with stack traces?',
        'answer': 'Source maps map transpiled code back to the original source so stack traces are easier to read.',
        'code': textwrap.dedent('''
            // Ensure devtool: 'source-map' is enabled in your bundler configuration
        ''')
    },
    {
        'prompt': 'How can I compress response bodies with zlib?',
        'answer': 'Pipe responses through zlib gzip to reduce payload size over the network.',
        'code': textwrap.dedent('''
            const zlib = require('zlib')
            const gzip = zlib.createGzip()
            response.pipe(gzip).pipe(res)
        ''')
    },
    {
        'prompt': 'How do I use Docker environment variables securely?',
        'answer': 'Pass secrets through environment variables or Docker secrets, not hardcode them in images.',
        'code': textwrap.dedent('''
            const dbUrl = process.env.DATABASE_URL
            console.log('connected to', dbUrl)
        ''')
    },
    {
        'prompt': 'How do I run a GitHub Actions workflow for Node.js?',
        'answer': 'Define a workflow file that checks out code, installs dependencies, and runs tests.',
        'code': textwrap.dedent('''
            name: CI
            on: [push]
            jobs:
              test:
                runs-on: ubuntu-latest
                steps:
                  - uses: actions/checkout@v2
        ''')
    },
    {
        'prompt': 'How do I proxy requests through Nginx for a Node app?',
        'answer': 'Configure Nginx to forward HTTP requests to your app server on a local port.',
        'code': textwrap.dedent('''
            server {
              location / {
                proxy_pass http://localhost:3000;
              }
            }
        ''')
    },
    {
        'prompt': 'How do I upload a file to AWS S3 in Node?',
        'answer': 'Use the AWS SDK putObject or upload method to send file data to S3.',
        'code': textwrap.dedent('''
            await s3.putObject({ Bucket: 'bucket', Key: 'file.txt', Body: data })
        ''')
    },
    {
        'prompt': 'How do I call the OpenAI API with fetch?',
        'answer': 'Send a JSON request to the OpenAI endpoint and parse the JSON response.',
        'code': textwrap.dedent('''
            fetch('https://api.openai.com/v1/chat/completions', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ model: 'gpt-4', messages: [] }),
            })
        ''')
    },
    {
        'prompt': 'How do I bridge Electron renderer and main processes?',
        'answer': 'Use ipcRenderer and ipcMain to exchange messages between renderer and main.',
        'code': textwrap.dedent('''
            ipcRenderer.send('get-data')
            ipcMain.on('get-data', event => event.reply('data', {}))
        ''')
    },
    {
        'prompt': 'How can a PWA detect offline status?',
        'answer': 'Use navigator.onLine and online/offline events to update application state.',
        'code': textwrap.dedent('''
            window.addEventListener('offline', () => console.log('offline'))
            window.addEventListener('online', () => console.log('online'))
        ''')
    },
    {
        'prompt': 'How do I establish a WebRTC peer connection?',
        'answer': 'Create RTCPeerConnection and exchange offer/answer SDP with a signaling channel.',
        'code': textwrap.dedent('''
            const pc = new RTCPeerConnection()
            pc.onicecandidate = event => console.log(event.candidate)
        ''')
    },
    {
        'prompt': 'How do I create a basic Three.js scene?',
        'answer': 'Initialize a scene, camera, renderer, and animate the render loop.',
        'code': textwrap.dedent('''
            const scene = new THREE.Scene()
            const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
            const renderer = new THREE.WebGLRenderer()
        ''')
    },
    {
        'prompt': 'How do I improve accessibility with ARIA attributes?',
        'answer': 'Use aria-label and role attributes to make UI controls understandable to assistive tech.',
        'code': textwrap.dedent('''
            const button = document.createElement('button')
            button.setAttribute('aria-label', 'Close')
        ''')
    },
    {
        'prompt': 'How do I internationalize static text in a JavaScript app?',
        'answer': 'Store translations in a dictionary and select the right text from the current locale.',
        'code': textwrap.dedent('''
            const messages = { en: 'Hello', es: 'Hola' }
            console.log(messages[locale])
        ''')
    },
    {
        'prompt': 'How do you animate with requestAnimationFrame?',
        'answer': 'Use requestAnimationFrame and update the next frame iteratively for smooth animation.',
        'code': textwrap.dedent('''
            function animate() {
              draw()
              requestAnimationFrame(animate)
            }
            animate()
        ''')
    },
    {
        'prompt': 'How do I access the microphone with MediaDevices?',
        'answer': 'Call navigator.mediaDevices.getUserMedia and handle the returned stream.',
        'code': textwrap.dedent('''
            navigator.mediaDevices.getUserMedia({ audio: true })
              .then(stream => console.log('microphone ready'))
        ''')
    },
    {
        'prompt': 'How do I scan Bluetooth devices from the browser?',
        'answer': 'Use navigator.bluetooth.requestDevice and filter by services or name.',
        'code': textwrap.dedent('''
            navigator.bluetooth.requestDevice({ acceptAllDevices: true })
        ''')
    },
    {
        'prompt': 'How do I process binary data with ArrayBuffer?',
        'answer': 'Use ArrayBuffer and TypedArray views to read and write binary bytes.',
        'code': textwrap.dedent('''
            const buffer = new ArrayBuffer(8)
            const view = new Uint8Array(buffer)
        ''')
    },
    {
        'prompt': 'How do I implement exponential backoff for retries?',
        'answer': 'Increase the delay between retries exponentially to avoid overwhelming the service.',
        'code': textwrap.dedent('''
            let delay = 100
            for (let attempt = 1; attempt <= 3; attempt += 1) {
              await wait(delay)
              delay *= 2
            }
        ''')
    },
    {
        'prompt': 'How do cookies differ from tokens for authentication?',
        'answer': 'Cookies are sent automatically by the browser, while tokens are usually stored and added manually to requests.',
        'code': textwrap.dedent('''
            fetch('/api', { headers: { Authorization: `Bearer ${token}` } })
        ''')
    },
    {
        'prompt': 'How do I protect against CSRF in form submissions?',
        'answer': 'Include a CSRF token in the form and validate it on the server before processing the request.',
        'code': textwrap.dedent('''
            form.append('csrf', csrfToken)
        ''')
    },
    {
        'prompt': 'How do I sanitize user input before rendering it?',
        'answer': 'Escape dangerous characters or use a safe rendering method to prevent injection attacks.',
        'code': textwrap.dedent('''
            const safe = input.replace(/[<>]/g, '')
        ''')
    },
    {
        'prompt': 'How do I prevent hydration mismatches in React?',
        'answer': 'Ensure the initial server-rendered markup matches the client render and delay browser-only code until after hydration.',
        'code': textwrap.dedent('''
            useEffect(() => {
              setClient(true)
            }, [])
        ''')
    },
    {
        'prompt': 'How do I read route parameters with React Router?',
        'answer': 'Use useParams to access route variables inside a component.',
        'code': textwrap.dedent('''
            const { id } = useParams()
            console.log(id)
        ''')
    },
    {
        'prompt': 'How do I create a simple in-memory cache with Map?',
        'answer': 'Store computed values in a Map and return them for repeated lookups.',
        'code': textwrap.dedent('''
            const cache = new Map()
            cache.set('key', 'value')
        ''')
    },
]

suffixes = [
    'in production',
    'for a fast web app',
    'when requests are frequent',
    'in a browser environment',
    'with strict mode enabled',
    'with secure defaults',
    'for accessibility',
    'for server-side rendering',
    'for offline use',
    'for testing',
    'for mobile devices',
    'with retry logic',
    'for observability',
    'with caching',
    'using functional style',
    'using typed annotations',
    'under heavy load',
    'with error boundaries',
    'for SEO-friendly pages',
    'with graceful shutdown',
]

suffix_variants = {
    'in production': {
        'addition': textwrap.dedent('''
            if (typeof process !== 'undefined' && process.env.NODE_ENV === 'production') {
              console.log('production ready')
            }
        ''')
    },
    'for a fast web app': {
        'addition': textwrap.dedent('''
            if (typeof performance !== 'undefined') {
              const start = performance.now()
              console.log('render time', performance.now() - start)
            }
        ''')
    },
    'when requests are frequent': {
        'addition': textwrap.dedent('''
            let lastRequest = 0
            const minInterval = 100
            if (Date.now() - lastRequest < minInterval) {
              console.log('skipping frequent request')
            }
        ''')
    },
    'in a browser environment': {
        'addition': textwrap.dedent('''
            if (typeof window !== 'undefined') {
              console.log('browser environment detected')
            }
        ''')
    },
    'with strict mode enabled': {
        'addition': textwrap.dedent('''
            'use strict'
        ''')
    },
    'with secure defaults': {
        'addition': textwrap.dedent('''
            const options = { secure: true, sameSite: 'lax' }
            console.log('secure defaults applied', options)
        ''')
    },
    'for accessibility': {
        'addition': textwrap.dedent('''
            const button = document.createElement('button')
            button.setAttribute('aria-label', 'Submit')
        ''')
    },
    'for server-side rendering': {
        'addition': textwrap.dedent('''
            const isServer = typeof window === 'undefined'
            if (isServer) {
              console.log('rendering on server')
            }
        ''')
    },
    'for offline use': {
        'addition': textwrap.dedent('''
            if (typeof navigator !== 'undefined' && !navigator.onLine) {
              console.log('offline mode enabled')
            }
        ''')
    },
    'for testing': {
        'addition': textwrap.dedent('''
            // This example is structured for tests and assertions
            const result = fn()
            expect(result).toBeDefined()
        ''')
    },
    'for mobile devices': {
        'addition': textwrap.dedent('''
            if (typeof window !== 'undefined' && window.matchMedia('(pointer: coarse)').matches) {
              console.log('mobile device layout')
            }
        ''')
    },
    'with retry logic': {
        'addition': textwrap.dedent('''
            let retries = 0
            const maxRetries = 3
            while (retries < maxRetries) {
              retries += 1
            }
        ''')
    },
    'for observability': {
        'addition': textwrap.dedent('''
            console.time('operation')
            console.timeEnd('operation')
        ''')
    },
    'with caching': {
        'addition': textwrap.dedent('''
            const cache = new Map()
            cache.set('key', 'value')
        ''')
    },
    'using functional style': {
        'addition': textwrap.dedent('''
            const compute = x => x * 2
            console.log(compute(5))
        ''')
    },
    'using typed annotations': {
        'addition': textwrap.dedent('''
            /** @type {number} */
            const count = 0
        ''')
    },
    'under heavy load': {
        'addition': textwrap.dedent('''
            const active = 120
            if (active > 100) {
              console.log('under heavy load')
            }
        ''')
    },
    'with error boundaries': {
        'addition': textwrap.dedent('''
            try {
              doWork()
            } catch (error) {
              console.error('boundary caught', error)
            }
        ''')
    },
    'for SEO-friendly pages': {
        'addition': textwrap.dedent('''
            if (typeof document !== 'undefined') {
              document.title = 'SEO friendly page'
            }
        ''')
    },
    'with graceful shutdown': {
        'addition': textwrap.dedent('''
            process.on('SIGTERM', () => {
              console.log('shutdown gracefully')
            })
        ''')
    },
}


def make_prompt(prompt, suffix):
    return f"{prompt[:-1]} {suffix}?" if prompt.endswith('?') else f"{prompt} {suffix}"


def make_variant_code(code, suffix):
    code = code.rstrip()
    addition = suffix_variants.get(suffix, {}).get('addition', '').strip()
    if suffix == 'with strict mode enabled':
        if code.startswith("'use strict'"):
            return code
        return f"'use strict'\n{code}"
    return f"{code}\n{addition}" if addition else code

entries = []
for template in base_templates:
    for suffix in suffixes:
        prompt = make_prompt(template['prompt'], suffix)
        code = make_variant_code(template['code'], suffix)
        entries.append((prompt, template['answer'], code))

output_entries = entries[:1000]

if len(output_entries) != 1000:
    raise SystemExit(f'Corpus does not contain 1000 segments: {len(output_entries)}')
if len({prompt for prompt, _, _ in output_entries}) != 1000:
    raise SystemExit('Duplicate prompts detected')
if len({code for _, _, code in output_entries}) != 1000:
    raise SystemExit('Duplicate code detected')

lines = []
for prompt, answer, code in output_entries:
    lines.append(f'USER: {prompt}')
    lines.append(f'ASSISTANT: {answer}')
    lines.append('--- INSTRUCTION ---')
    lines.append('```js')
    lines.append(code.strip())
    lines.append('```')
    lines.append('--- RESPONSE ---')
    lines.append('')

output = Path('docs/corpus_generated.txt')
output.write_text('\n'.join(lines).strip() + '\n', encoding='utf-8')
print('wrote', output)
print('segments', len(output_entries))
print('unique prompts', len({prompt for prompt, _, _ in output_entries}))
print('unique code blocks', len({code for _, _, code in output_entries}))
