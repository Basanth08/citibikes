# 🏗️ **Project Structure Guide**

> **Professional organization for data engineers at all levels**

---

## 📁 **Directory Structure Overview**

```
citibikes/
├── 📁 src/                          # Source code (main application)
│   ├── 📁 core/                     # Core application logic
│   │   ├── main.py                  # Main producer application
│   │   ├── consume.py               # Main consumer application
│   │   ├── config.py                # Configuration management
│   │   └── 📁 bikes_module/         # Business logic for bike data
│   ├── 📁 streaming/                # Real-time streaming components
│   │   ├── 📁 kafka_producer/       # Kafka producer implementation
│   │   └── 📁 kafka_consumer/       # Kafka consumer implementation
│   ├── 📁 aws/                      # AWS cloud integration
│   │   ├── aws_upload.py            # S3 log upload automation
│   │   ├── setup_glue.py            # Glue database & crawler setup
│   │   ├── query_athena.py          # Athena SQL queries
│   │   ├── create_s3_bucket.py      # S3 bucket creation
│   │   ├── create_glue_role.py      # IAM role creation
│   │   ├── update_crawler.py        # Crawler configuration updates
│   │   ├── start_crawler.py         # Manual crawler execution
│   │   ├── check_crawler_status.py  # Crawler monitoring
│   │   ├── list_tables.py           # Glue table listing
│   │   ├── get_table_schema.py      # Table schema inspection
│   │   └── list_s3_contents.py      # S3 bucket contents
│   └── 📁 utils/                    # Utility components
│       ├── 📁 services/             # HTTP and other services
│       └── 📁 constants/            # Application constants
├── 📁 config/                       # Configuration files
│   ├── docker-compose.yaml          # Local infrastructure setup
│   ├── requirements.txt              # Python dependencies
│   ├── aws_config.env               # AWS configuration
│   └── aws_config.env.backup        # AWS config backup
├── 📁 scripts/                      # Automation and utility scripts
│   ├── 📁 setup/                    # Setup and installation scripts
│   ├── 📁 aws/                      # AWS-specific scripts
│   └── 📁 monitoring/               # Monitoring and health checks
├── 📁 docs/                         # Documentation and diagrams
│   ├── 📁 architecture/             # System architecture diagrams
│   ├── 📁 api/                      # API documentation
│   ├── 📁 deployment/               # Deployment guides
│   └── 📁 images/                   # Architecture and flow diagrams
├── 📁 tests/                        # Testing framework
│   ├── 📁 unit/                     # Unit tests
│   ├── 📁 integration/              # Integration tests
│   └── test_pipeline.py             # Main test suite
├── 📁 examples/                     # Usage examples and samples
├── 📁 logs/                         # Application log files
├── README.md                         # Main project documentation
└── PROJECT_STRUCTURE.md              # This file
```

---

## 🎯 **What Each Directory Contains**

### **📁 `src/` - Source Code**
**Purpose**: Main application code organized by functionality

**For Beginners**: Start here to understand the core application
**For Experienced**: Review architecture patterns and implementation details

#### **📁 `src/core/` - Core Application**
- **`main.py`**: Entry point for the data producer
- **`consume.py`**: Entry point for the data consumer  
- **`config.py`**: Centralized configuration management
- **`bikes_module/`**: Business logic and data models

#### **📁 `src/streaming/` - Real-time Data Processing**
- **`kafka_producer/`**: Kafka message publishing
- **`kafka_consumer/`**: Kafka message consumption
- **Key Concepts**: Message queuing, fault tolerance, scalability

#### **📁 `src/aws/` - Cloud Integration**
- **S3 Operations**: Data storage and management
- **Glue Operations**: Schema discovery and metadata
- **Athena Operations**: SQL analytics on S3 data
- **IAM Management**: Security and access control

#### **📁 `src/utils/` - Shared Components**
- **`services/`**: HTTP clients and external integrations
- **`constants/`**: Application-wide constants and settings

### **📁 `config/` - Configuration Management**
**Purpose**: All configuration files in one place

**For Beginners**: Environment setup and basic configuration
**For Experienced**: Infrastructure as code and environment management

- **`docker-compose.yaml`**: Local development infrastructure
- **`requirements.txt`**: Python package dependencies
- **`aws_config.env`**: AWS service configuration

### **📁 `scripts/` - Automation & Utilities**
**Purpose**: Scripts for setup, deployment, and maintenance

**For Beginners**: Use these to get started quickly
**For Experienced**: Extend and customize for production use

- **`setup/`**: Installation and environment setup
- **`aws/`**: AWS resource management automation
- **`monitoring/`**: Health checks and system monitoring

### **📁 `docs/` - Documentation**
**Purpose**: Comprehensive project documentation

**For Beginners**: Start here to understand the system
**For Experienced**: Reference for architecture decisions and patterns

- **`architecture/`**: System design and flow diagrams
- **`api/`**: API specifications and usage examples
- **`deployment/`**: Production deployment guides
- **`images/`**: Visual representations of the system

### **📁 `tests/` - Quality Assurance**
**Purpose**: Automated testing and validation

**For Beginners**: Learn testing best practices
**For Experienced**: Ensure code quality and reliability

- **`unit/`**: Individual component testing
- **`integration/`**: End-to-end system testing
- **`test_pipeline.py`**: Main test suite

### **📁 `examples/` - Usage Examples**
**Purpose**: Practical examples and use cases

**For Beginners**: Learn by example
**For Experienced**: Reference implementations and patterns

### **📁 `logs/` - Application Logs**
**Purpose**: Operational data and debugging information

**For Beginners**: Understand system behavior
**For Experienced**: Monitor and troubleshoot production issues

---

## 🚀 **How to Navigate This Project**

### **👶 Beginner Level (0-1 years experience)**
1. **Start with**: `README.md` → `docs/` → `src/core/main.py`
2. **Focus on**: Understanding the data flow and basic concepts
3. **Key files**: `main.py`, `consume.py`, `config.py`
4. **Goal**: Get the system running and understand what it does

### **👨‍💻 Intermediate Level (1-3 years experience)**
1. **Start with**: `src/streaming/` → `src/utils/` → `tests/`
2. **Focus on**: Architecture patterns and implementation details
3. **Key files**: All files in `src/streaming/`, `docker-compose.yaml`
4. **Goal**: Understand the system design and extend functionality

### **👨‍🔬 Advanced Level (3+ years experience)**
1. **Start with**: `src/aws/` → `config/` → `scripts/`
2. **Focus on**: Production deployment and cloud architecture
3. **Key files**: All AWS integration files, configuration management
4. **Goal**: Deploy to production and optimize performance

---

## 🔧 **Key Files to Understand**

### **Entry Points**
- **`src/core/main.py`**: Producer application entry point
- **`src/core/consume.py`**: Consumer application entry point

### **Configuration**
- **`config/docker-compose.yaml`**: Local infrastructure setup
- **`config/aws_config.env`**: AWS service configuration
- **`src/core/config.py`**: Application configuration management

### **Core Logic**
- **`src/core/bikes_module/bikes.py`**: Business logic implementation
- **`src/streaming/kafka_producer/producer.py`**: Data publishing
- **`src/streaming/kafka_consumer/consumer.py`**: Data consumption

### **Cloud Integration**
- **`src/aws/aws_upload.py`**: S3 data upload automation
- **`src/aws/setup_glue.py`**: AWS Glue setup and management
- **`src/aws/query_athena.py`**: SQL analytics on cloud data

---

## 📚 **Learning Path by Experience Level**

### **Week 1: Foundation**
- Read `README.md` completely
- Set up local environment with `config/docker-compose.yaml`
- Run `src/core/main.py` and `src/core/consume.py`

### **Week 2: Understanding**
- Study `src/core/bikes_module/bikes.py`
- Explore `src/streaming/` components
- Run tests in `tests/test_pipeline.py`

### **Week 3: Extension**
- Modify configuration in `src/core/config.py`
- Add new data fields in `src/core/bikes_module/`
- Create new tests in `tests/`

### **Week 4: Cloud Integration**
- Set up AWS environment with `config/aws_config.env`
- Run AWS setup scripts in `src/aws/`
- Execute cloud analytics with `src/aws/query_athena.py`

---

## 🎯 **Best Practices Demonstrated**

### **Code Organization**
- **Separation of Concerns**: Each module has a single responsibility
- **Package Structure**: Logical grouping of related functionality
- **Import Management**: Clean import statements and dependencies

### **Configuration Management**
- **Environment Variables**: Secure credential management
- **Centralized Config**: Single source of truth for settings
- **Infrastructure as Code**: Docker and AWS automation

### **Testing & Quality**
- **Test Organization**: Unit and integration test separation
- **Automated Testing**: Comprehensive test coverage
- **Quality Assurance**: Code quality and validation

### **Documentation**
- **Comprehensive README**: Clear setup and usage instructions
- **Code Comments**: Inline documentation and explanations
- **Architecture Diagrams**: Visual system representation

---

## 🚨 **Common Pitfalls & Solutions**

### **Import Errors**
- **Problem**: Module not found errors
- **Solution**: Ensure you're running from project root directory
- **Prevention**: Use relative imports and proper package structure

### **Configuration Issues**
- **Problem**: Environment variables not loaded
- **Solution**: Check `config/aws_config.env` and source it properly
- **Prevention**: Use configuration validation and defaults

### **Docker Issues**
- **Problem**: Services not starting
- **Solution**: Check `config/docker-compose.yaml` and Docker logs
- **Prevention**: Verify Docker Desktop is running and has sufficient resources

### **AWS Permission Errors**
- **Problem**: Access denied to AWS services
- **Solution**: Verify IAM roles and permissions in `src/aws/create_glue_role.py`
- **Prevention**: Use principle of least privilege and test permissions

---

## 🔮 **Next Steps & Extensions**

### **Immediate Improvements**
1. **Add logging configuration** in `config/`
2. **Create monitoring scripts** in `scripts/monitoring/`
3. **Add data validation** in `src/core/bikes_module/`

### **Advanced Features**
1. **Real-time dashboards** using Grafana or QuickSight
2. **Machine learning integration** for demand prediction
3. **Multi-region deployment** for global scalability

### **Production Readiness**
1. **CI/CD pipeline** for automated testing and deployment
2. **Monitoring and alerting** with CloudWatch
3. **Security hardening** with KMS and VPC isolation

---

**This project structure demonstrates professional software engineering practices and provides a clear learning path for data engineers at all experience levels.** 