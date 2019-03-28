package com.trackback.demo.DAO;

import com.trackback.demo.bean.Route;
import org.springframework.data.jpa.repository.JpaRepository;

import java.sql.Timestamp;
import java.util.List;

public interface RouteRepository extends JpaRepository<Route, Integer> {
    List<Route> findAllByDriveridAndTimeBetween(int driverid, Timestamp after, Timestamp before);

}
