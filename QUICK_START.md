# 🚀 **Quick Start Guide**

> **Get your Citibikes data pipeline running in 5 minutes!**

---

## ⚡ **5-Minute Setup**

### **1. Clone & Navigate**
```bash
git clone <your-repository-url>
cd citibikes
```

### **2. One-Command Setup**
```bash
./scripts/setup/install.sh
```

### **3. Start the Pipeline**
```bash
# Terminal 1: Start producer
python src/core/main.py

# Terminal 2: Start consumer  
python src/core/consume.py
```

### **4. Verify It's Working**
```bash
# Check logs
tail -f logs/citibikes_pipeline.log
tail -f logs/citibikes_consumer.log

# Health check
./scripts/monitoring/health_check.sh
```

---

## 🎯 **What You'll See**

- **Real-time bike data** streaming from CitiBikes API
- **Kafka messages** being produced and consumed
- **Structured logs** with timestamps and data details
- **Live metrics** and performance data

---

## 🔧 **Troubleshooting**

### **Common Issues**
- **Docker not running**: Start Docker Desktop
- **Port conflicts**: Check if ports 9092/2181 are free
- **Python errors**: Run `pip install -r config/requirements.txt`

### **Get Help**
```bash
# Comprehensive health check
./scripts/monitoring/health_check.sh

# Performance metrics
./scripts/monitoring/metrics_collector.sh

# View project structure
cat PROJECT_STRUCTURE.md
```

---

## 📚 **Next Steps**

1. **Explore the code**: Check `src/core/` and `src/streaming/`
2. **Modify data**: Edit `src/core/config.py` for different settings
3. **Add features**: Extend `src/core/bikes_module/bikes.py`
4. **Go cloud**: Run `./scripts/aws/setup_aws.sh` for AWS integration

---

**🎉 You're all set! Your real-time data pipeline is now running.**

*For detailed instructions, see the full README.md or PROJECT_STRUCTURE.md* 