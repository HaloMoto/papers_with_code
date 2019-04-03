package com.trackback.demo.DAO;

import com.trackback.demo.bean.Schedule;
import org.springframework.data.jpa.repository.JpaRepository;

import java.sql.Timestamp;
import java.util.List;

public interface ScheduleRepository extends JpaRepository<Schedule, Integer> {
    List<Schedule> findAllByDriveridAndTimeBetweenOrderByTimeAsc(int driverid, Timestamp after, Timestamp before);
}
