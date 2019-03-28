package com.trackback.demo.controller;

import com.trackback.demo.DAO.RouteRepository;
import com.trackback.demo.DAO.ScheduleRepository;
import com.trackback.demo.bean.Route;
import com.trackback.demo.bean.Schedule;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import java.sql.Timestamp;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
public class DriverController {
    @Autowired
    private RouteRepository routeRepository;

    @Autowired
    private ScheduleRepository scheduleRepository;

    @RequestMapping(value = {"/","trackback_one"})
    public String traceback_one(){
        return "trackback_one";
    }

    @RequestMapping(value = {"trackback_many"})
    public String traceback_many(){
        return "trackback_many";
    }

    @RequestMapping(value = "/searchDriver", method = RequestMethod.GET, produces = "application/json;charset=UTF-8")
    public String search_driver(int driverid, Timestamp after, Timestamp before, Model model){
        model.addAttribute("route", routeRepository.findAllByDriveridAndTimeBetween(driverid, after, before));
        model.addAttribute("schedule", scheduleRepository.findAllByDriveridAndTimeBetween(driverid, after, before));
        System.out.println(after);
        System.out.println(before);
        return "lushu";
    }

    @RequestMapping(value = "/searchDrivers", method = RequestMethod.GET, produces = "application/json;charset=UTF-8")
    public String search_drivers(int driverid_start, int driverid_end, Timestamp after, Timestamp before, Model model){
        model.addAttribute("driverid_start", driverid_start);
        model.addAttribute("driverid_end", driverid_end);
        Map<Integer, List<Route>> route = new HashMap();
        Map<Integer, List<Schedule>> schedule = new HashMap();
        for (int i = driverid_start; i < driverid_end; i++){
            route.put(i, routeRepository.findAllByDriveridAndTimeBetween(i, after, before));
            schedule.put(i, scheduleRepository.findAllByDriveridAndTimeBetween(i, after, before));
        }
        model.addAttribute("route", route);
        model.addAttribute("schedule", schedule);

        return "reli";
    }

}
