package br.edu.ufcg.computacao.eureca.backend.core.models.mapentries;

import java.util.ArrayList;
import java.util.Collection;

public class StudentEnrollment extends EurecaMultivaluedMapValue {
    Collection<StudentPerformance> performances;

    public StudentEnrollment(Collection<StudentPerformance> performances) {
        this.performances = performances;
    }

    public StudentEnrollment() {
        this.performances = new ArrayList<>();
    }

    @Override
    public Collection<StudentPerformance> getCollection() {
        return this.performances;
    }
    
    public Collection<StudentPerformance> getPerformances() {
        return performances;
    }

    public void setPerformances(Collection<StudentPerformance> performances) {
        this.performances = performances;
    }
}
