package br.edu.ufcg.computacao.eureca.backend.core.models.mapentries;

import java.util.ArrayList;
import java.util.Collection;

public class EnrollmentTeacher extends EurecaMultivaluedMapValue {
    Collection<SiapeValue> teachers;

    public EnrollmentTeacher(Collection<SiapeValue> teachers) {
        this.teachers = teachers;
    }

    public EnrollmentTeacher() {
        this.teachers = new ArrayList<>();
    }

    @Override
    public Collection<SiapeValue> getCollection() {
        return this.teachers;
    }
    
    public Collection<SiapeValue> getTeachers() {
        return teachers;
    }

    public void setTeachers(Collection<SiapeValue> teachers) {
        this.teachers = teachers;
    }
}
