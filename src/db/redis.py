from redis import asyncio as redis
from src.config import Config

token_blocklist = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    decode_responses=True
)
from src.config import Config

"""Deep explanation

A Redis client is a library/package in your programming language that lets your application talk to a Redis server.

Think of it like this:

FastAPI app  <--Redis Client-->  Redis Server

Without a Redis client:

Your FastAPI app doesn't know how to send commands to Redis.
You cannot do things like:
SET user:1 "John"
GET user:1
DEL user:1

The client converts your Python code into Redis commands and sends them to the Redis server.

Real-world analogy

Imagine Redis is a restaurant kitchen.

Kitchen → Redis server
You → FastAPI app
Waiter → Redis client

You don't walk into the kitchen and cook directly.

You tell the waiter:

Bring me coffee

The waiter communicates with the kitchen and returns:

Coffee delivered

Redis client does the same thing.

In Python (FastAPI)

You usually install a Redis client:

pip install redis

Then use it:

import redis

client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

client.set("name", "Manikanta")

value = client.get("name")

print(value)

What happens internally:

client.set("name","Manikanta")
        ↓
Redis client sends:
SET name "Manikanta"
        ↓
Redis server stores it
What Redis helps us do

Redis is extremely fast because it stores data in memory (RAM).

Common uses:

1. Caching

Instead of repeatedly querying the database:

User requests profile
      ↓
Database queried every time ❌

Use Redis:

First request
Database → Redis cache

Next requests
Redis → return data instantly

Example:

cached_user = client.get("user:123")

if not cached_user:
    user = fetch_from_db()
    client.set("user:123", user)

Benefit:

Faster responses
Less database load
2. Store JWT tokens / blacklisted tokens

In authentication systems:

User logs out
↓
Store token in Redis blacklist
↓
Reject token if used again

Useful because JWTs are stateless by default.

3. Session management

Store login sessions:

session:user123 → active
4. Rate limiting

Prevent spam:

User made 20 requests in 1 minute
↓
Block further requests

Redis can count quickly:

client.incr("user:123")
5. Queues / background jobs

For example:

User uploads image
↓
Add task to Redis queue
↓
Worker processes image later
In FastAPI projects, Redis commonly appears like:
from redis.asyncio import Redis

redis_client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

Then:

await redis_client.set(
    "access_token",
    token
)

token = await redis_client.get(
    "access_token"
)
Interview-style answer

A Redis client is a language-specific library used to communicate with a Redis server. 
It helps applications perform Redis operations such as storing, retrieving, updating, and deleting data. 
Redis clients are commonly used for caching, session storage, authentication token handling, rate limiting, and message queues.

what wxactly is this redis 

No — hidden memory would not materially change this explanation.

Deep explanation

Redis stands for:

REmote DIctionary Server

Redis is an in-memory database / key-value data store.

"In-memory" means:

Normal database (MySQL/PostgreSQL)
        ↓
Stores data on disk (SSD/HDD)

Redis
        ↓
Stores data in RAM

RAM is much faster than disk storage.

That is why Redis can handle operations in microseconds to milliseconds.

Think of Redis as a giant Python dictionary on a server

Python dictionary:

data = {
    "name": "Manikanta",
    "age": 20
}

Access:

print(data["name"])

Output:

Manikanta

Redis works similarly:

SET name "Manikanta"
SET age 20
GET name

Output:

Manikanta

So Redis is basically:

key  → value

Example:

"user:101" → "John"
"token:123" → "abcxyz"
"views" → 500
Why not just use a normal database?

Suppose a user opens Instagram:

Without Redis:

User request
    ↓
Database query (disk access)
    ↓
Return result

Doing this millions of times creates load.

With Redis:

User request
    ↓
Redis (RAM)
    ↓
Return immediately

Very fast.

Redis is not limited to strings

It can store multiple data structures:

Redis Type	Example
String	"John"
List	["a","b","c"]
Hash	{name:"John", age:20}
Set	{1,2,3}
Sorted Set	rankings/leaderboards
Streams	message data

Examples:

String:

SET username "John"

List:

LPUSH fruits apple
LPUSH fruits mango

Hash:

HSET user name John
HSET user age 20
Why FastAPI projects use Redis a lot
Authentication

Store refresh tokens:

refresh_token:user123
Caching

Store frequently used data:

product:10
Rate limiting

Count requests:

user:123:requests
Background jobs

Queue tasks:

send_email_task
Sessions

Store login session information:

session:user123
Where Redis runs

Redis itself is a separate server process:

Your FastAPI App
        ↓
Redis Client
        ↓
Redis Server
        ↓
RAM

You usually start it like:

redis-server

or with Docker:

docker run -p 6379:6379 redis

Port 6379 is Redis's default port.

Interview-style answer

Redis is an in-memory key-value database that stores data in RAM for extremely 
fast read and write operations. It is commonly used for caching, session management,
 authentication token storage, rate limiting, queues, and real-time applications."""





JTI_EXPIRY = 3600




async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti:str) -> bool:
   jti =  await token_blocklist.get(jti)

   return jti is not None