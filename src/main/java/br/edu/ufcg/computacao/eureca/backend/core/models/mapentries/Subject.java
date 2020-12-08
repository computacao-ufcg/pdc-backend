package br.edu.ufcg.computacao.eureca.backend.core.models.mapentries;

public class Subject extends EurecaMapValue {
    long subjectCode;
    String term;
    int credits;
    int hours;
    String subjectName;
    String subjectType;
    String status;

    public Subject(long subjectCode, String term, int credits, int hours, String subjectName,
                   String subjectType, String status) {
        this.subjectCode = subjectCode;
        this.term = term;
        this.credits = credits;
        this.hours = hours;
        this.subjectName = subjectName;
        this.subjectType = subjectType;
        this.status = status;
    }

    public Subject() {
    }

    public long getSubjectCode() {
        return subjectCode;
    }

    public void setSubjectCode(long subjectCode) {
        this.subjectCode = subjectCode;
    }

    public String getTerm() {
        return term;
    }

    public void setTerm(String term) {
        this.term = term;
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

    public String getSubjectName() {
        return subjectName;
    }

    public void setSubjectName(String subjectName) {
        this.subjectName = subjectName;
    }

    public String getSubjectType() {
        return subjectType;
    }

    public void setSubjectType(String subjectType) {
        this.subjectType = subjectType;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    @Override
    public String toString() {
        return "Subject{" +
                "subjectCode=" + subjectCode +
                ", term='" + term + '\'' +
                ", credits=" + credits +
                ", hours=" + hours +
                ", subjectName='" + subjectName + '\'' +
                ", subjectType='" + subjectType + '\'' +
                ", status='" + status + '\'' +
                '}';
    }
}