package br.edu.ufcg.computacao.eureca.backend.core.models.mapentries;

public class SubjectData extends EurecaMapValue {
    String code;
    int type_id;
    int credits;
    int hours;
    String name;

    public SubjectData(String code, int type_id, int credits, int hours, String name) {
        this.code = code;
        this.type_id = type_id;
        this.credits = credits;
        this.hours = hours;
        this.name = name;
    }

    public SubjectData() {
    }

    public int getCredits() {
        return credits;
    }

    public void setCredits(int credits) {
        this.credits = credits;
    }

    public int getHours() {
        return hours;
    }

    public void setHours(int hours) {
        this.hours = hours;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getType_id() {
        return type_id;
    }

    public void setType_id(int type_id) {
        this.type_id = type_id;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    @Override
    public String toString() {
        return code + ":" + type_id + ":" + credits + ":" + hours + ":" + name;
    }
}
