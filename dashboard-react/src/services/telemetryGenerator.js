class F1TelemetryGenerator {
  constructor() {
    this.lapTime = 0;
    this.sector = 1;
    this.position = { x: 0, y: 0 };
    this.speed = 0;
    this.rpm = 0;
    this.gear = 1;
    this.throttle = 0;
    this.brake = 0;
    this.steering = 0;
    this.drs = false;
    this.ersDeployMode = "Medium";
    this.fuelRemaining = 100;
    this.tireTemps = { fl: 85, fr: 87, rl: 83, rr: 86 };
    this.tirePressures = { fl: 22.1, fr: 22.3, rl: 21.8, rr: 22.0 };
    this.trackRadius = 200;
    this.centerX = 300;
    this.centerY = 200;
    this.angle = 0;
    this.predictedPath = [];
    
    // Race tracking
    this.currentLap = 1;
    this.totalLaps = 58;
    this.bestLapTime = 82.123; // 1:22.123
    this.lapTimes = [];
    this.raceStartTime = Date.now();
    this.lastLapTime = 0;
    this.drivers = this.generateDrivers();
  }

  generateDrivers() {
    const driverNames = [
      "VER", "LEC", "NOR", "RUS", "PER", "SAI", "HAM", "ALO", 
      "OCO", "BOT", "GAS", "STR", "ALB", "MAG", "TSU", "HUL",
      "ZHO", "RIC", "PIA", "SAR"
    ];
    
    return driverNames.map((name, index) => ({
      id: index + 1,
      name: name,
      position: index + 1,
      currentLap: Math.floor(Math.random() * 3) + 1,
      lapTime: 82 + Math.random() * 5, // 1:22-1:27
      isCurrentDriver: index === 0
    }));
  }

  generateTelemetry() {
    // Simulate lap progression
    this.lapTime += 0.1;
    this.angle += 0.02;

    // Check for lap completion
    if (this.angle >= 2 * Math.PI) {
      this.completeLap();
      this.angle = 0;
    }

    // Generate track position (oval track)
    this.position.x = this.centerX + this.trackRadius * Math.cos(this.angle);
    this.position.y = this.centerY + this.trackRadius * Math.sin(this.angle);

    // Update sector based on angle
    if (this.angle < Math.PI * 2/3) {
      this.sector = 1;
    } else if (this.angle < Math.PI * 4/3) {
      this.sector = 2;
    } else {
      this.sector = 3;
    }

    // Generate realistic telemetry data
    this.speed = Math.floor(180 + Math.sin(this.angle * 2) * 50 + Math.random() * 20);
    this.rpm = Math.floor(8000 + (this.speed / 320) * 4000 + Math.random() * 200);
    this.gear = Math.min(8, Math.max(1, Math.floor(this.speed / 40)));
    this.throttle = Math.floor(20 + Math.random() * 80);
    this.brake = this.speed > 200 ? Math.floor(Math.random() * 80) : 0;
    this.steering = (Math.random() - 0.5) * 0.6;
    this.drs = Math.random() > 0.7 && this.speed > 250;
    this.fuelRemaining = Math.max(0, this.fuelRemaining - Math.random() * 0.02);

    // Tire temperature simulation
    Object.keys(this.tireTemps).forEach(tire => {
      this.tireTemps[tire] += (Math.random() - 0.5) * 4;
      this.tireTemps[tire] = Math.max(60, Math.min(120, this.tireTemps[tire]));
    });

    // Tire pressure simulation
    Object.keys(this.tirePressures).forEach(tire => {
      this.tirePressures[tire] += (Math.random() - 0.5) * 0.2;
      this.tirePressures[tire] = Math.max(20.0, Math.min(24.0, this.tirePressures[tire]));
    });

    // Update drivers' lap times
    this.updateDrivers();

    return {
      lapTime: this.lapTime,
      sector: this.sector,
      position: this.position,
      speed: this.speed,
      rpm: this.rpm,
      gear: this.gear,
      throttle: this.throttle,
      brake: this.brake,
      steering: this.steering,
      drs: this.drs,
      ersDeployMode: this.ersDeployMode,
      fuelRemaining: this.fuelRemaining,
      tireTemps: this.tireTemps,
      tirePressures: this.tirePressures,
      currentLap: this.currentLap,
      totalLaps: this.totalLaps,
      bestLapTime: this.bestLapTime,
      lapTimes: this.lapTimes,
      drivers: this.drivers,
      angle: this.angle
    };
  }

  completeLap() {
    this.currentLap++;
    const lapTime = this.lapTime;
    this.lapTimes.push(lapTime);
    
    // Update best lap time
    if (lapTime < this.bestLapTime) {
      this.bestLapTime = lapTime;
    }
    
    this.lapTime = 0;
  }

  updateDrivers() {
    // Simulate other drivers progressing
    this.drivers.forEach((driver) => {
      if (!driver.isCurrentDriver) {
        // Randomly advance other drivers
        if (Math.random() < 0.001) { // 0.1% chance per update
          driver.currentLap++;
          driver.lapTime = 82 + Math.random() * 5;
        }
      }
    });
  }

  formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = (seconds % 60).toFixed(3);
    return `${minutes}:${secs.padStart(6, '0')}`;
  }
}

export default F1TelemetryGenerator;

