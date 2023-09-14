"use client";
import React, { useState, useEffect } from "react";

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { Button } from "@/components/ui/button";

export default function Batches() {
  const [batchRecords, setbatchRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function downloadReports(batch_id: string) {
    try {
      const response = await fetch(
        `http://localhost:8000/batch_report/${batch_id}`
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${batch_id}.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove(); // Removing the anchor element after the download
    } catch (error) {
      console.error("Error downloading the file:", error);
    }
  }
  async function getBatchRecords() {
    setLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/batch_files`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const responseData = await response.json();
      setbatchRecords(responseData);
      setLoading(false);
    } catch (error: any) {
      setError(error);
      setLoading(false);
    }
  }
  useEffect(() => {
    // Call getBatchRecords once on component mount.
    getBatchRecords();
  }, []);

  return (
    <>
      Uploaded Files
      <Table>
        <TableCaption>A list of recently uploaded files.</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Batch</TableHead>
            <TableHead>Date Processed</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {batchRecords.map((record) => (
            <TableRow key={record._id}>
              <TableCell className="font-medium">{record._id}</TableCell>
              <TableCell>{record.date}</TableCell>
              <TableCell className="text-right">
                <Button onClick={() => downloadReports(record._id)}>
                  Download Reports
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  );
}
