# Distributed Task Scheduler (Python)

![Python CI](https://github.com/yourusername/distributed-task-scheduler/actions/workflows/python-app.yml/badge.svg)

A low-level, asyncio-based distributed task scheduler that coordinates workers to process tasks via a custom binary RPC protocol over TCP. This project demonstrates building a simple but efficient distributed computing system using Python's asyncio.

## 🚀 Features

- **Custom Binary Protocol**: Efficient binary RPC protocol with struct-based message encoding
- **Asynchronous Architecture**: Built with Python's asyncio for high-performance I/O
- **Distributed Processing**: Multiple workers can connect and process tasks in parallel
- **Fault Tolerance**: Graceful handling of worker disconnections and reconnections
- **Simple CLI**: Easy-to-use command-line interface for task submission
- **Zero Dependencies**: Uses only Python standard library modules

## 📋 Requirements

- Python 3.8+
- No external dependencies required

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │    │  Scheduler  │    │   Worker    │
│             │    │             │    │             │
│ Submit Task │───▶│  Queue &    │───▶│ Process &   │
│             │    │  Distribute │    │  Return     │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Components

- **Scheduler** (`server.py`): Coordinates task distribution and result collection
- **Worker** (`worker.py`): Processes tasks and returns results
- **Client** (`client.py`): Submits tasks to the scheduler
- **Protocol** (`lib/protocol.py`): Binary message encoding/decoding
- **Jobs** (`lib/jobs.py`): Task processing logic (SHA256 hashing)

## 🚀 Quick Start

### 1. Start the Scheduler

```bash
python server.py
```

The scheduler will start listening on port 9001.

### 2. Start Workers

In separate terminals, start one or more workers:

```bash
python worker.py
```

You can run multiple workers to increase processing capacity.

### 3. Submit Tasks

Submit tasks using the client:

```bash
python client.py "Hello, World!"
python client.py "Another string to hash"
```

## 📖 Usage Examples

### Basic Usage

```bash
# Terminal 1: Start scheduler
python server.py

# Terminal 2: Start worker
python worker.py

# Terminal 3: Submit task
python client.py "My string to hash"
```

### Multiple Workers

```bash
# Start multiple workers for parallel processing
python worker.py  # Worker 1
python worker.py  # Worker 2
python worker.py  # Worker 3
```

## 🔧 Protocol Details

The system uses a custom binary protocol:

- **Message Format**: `[1 byte command][4 bytes length][payload]`
- **Commands**:
  - `1`: Task assignment
  - `2`: Result submission
  - `3`: Hello/keepalive (reserved)

### Message Flow

1. **Task Submission**: Client → Scheduler (via queue)
2. **Task Assignment**: Scheduler → Worker (binary protocol)
3. **Task Processing**: Worker computes SHA256 hash
4. **Result Return**: Worker → Scheduler (binary protocol)

## 🛠️ Development

### Project Structure

```
distributed_task_scheduler/
├── server.py              # Main scheduler server
├── worker.py              # Worker process
├── client.py              # CLI client
├── lib/
│   ├── protocol.py        # Binary protocol implementation
│   ├── jobs.py           # Task processing functions
│   └── utils.py          # Utility functions
├── requirements.txt       # Dependencies (empty - stdlib only)
├── README.md             # This file
└── .github/workflows/    # CI/CD configuration
```

### Running Tests

```bash
# Currently uses a dummy test in CI
# Future: Add proper unit tests
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Future Enhancements

- [ ] Add proper unit tests
- [ ] Implement task result retrieval
- [ ] Add worker health monitoring
- [ ] Support for different task types
- [ ] Configuration file support
- [ ] Metrics and monitoring
- [ ] Docker containerization
