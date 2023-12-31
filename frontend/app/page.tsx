"use client";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Label } from "@/components/ui/label";
import React, { useState } from "react";
import { Loader2 } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import * as z from "zod";
import { Alert } from "@mui/material";

import { Button } from "@/components/ui/button";
import { Form, FormField, FormItem } from "@/components/ui/form";
import { Input } from "@/components/ui/input";

const FormSchema = z.object({
  // Improvement: require only XML files
  file: z.any(),
});

export default function Test() {
  const [pendingPayments, setPendingPayments] = useState([]);
  const [fileContent, setFileContent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState(null);
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
  });

  // Improvement: Convert to one function and streamline
  function onSubmit() {
    submitFile(fileContent);
  }

  // When a file is uploaded, grab the contents and store in state
  function handleFileChange(event: { target: { files: any[] } }) {
    setShowSuccess(false);

    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();

      reader.onload = function (e) {
        setFileContent(e.target.result);
      };

      reader.onerror = function (e) {
        console.error("Failed to read file:", e);
      };

      reader.readAsText(file);
    }
  }

  // Take file contents and process the XML file.
  // Response will be a list of pending payments
  async function submitFile(data: any) {
    setLoading(true);

    try {
      console.log("submitting file");
      const response = await fetch(`http://localhost:8000/upload_xml`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          payload: data,
        }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const responseData = await response.json();
      setPendingPayments(responseData);
      setLoading(false);
    } catch (error: any) {
      setError(error);
      setLoading(false);
    }
  }

  // Using the batch ID, make an api call to process pending payments
  async function processPayments(batch_id: string) {
    console.log("submitting file");
    setLoading(true);
    setShowSuccess(false);
    try {
      const response = await fetch(
        // URL should be moved to ENV to be dynamic by environment
        `http://localhost:8000/authorize_payments/${batch_id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      // Reset the statuses
      setLoading(false);
      setShowSuccess(true);
      setPendingPayments([]);
    } catch (error: any) {
      setError(error);
      setLoading(false);
    }
  }

  function centsToDollars(cents: number): string {
    return `$${(cents / 100).toFixed(2)}`;
  }

  return (
    <>
      <h1>Dashboard</h1>
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="w-2/3 space-y-6"
        >
          <FormField
            control={form.control}
            name="file"
            render={({ field }) => (
              <FormItem>
                <div className="grid w-full max-w-sm items-center gap-1.5">
                  <Label htmlFor="file">Please upload an xml file</Label>
                  <Input
                    id="file"
                    type="file"
                    {...field}
                    onChange={handleFileChange}
                  />
                </div>
              </FormItem>
            )}
          />
          {loading ? (
            <>
              <Button disabled>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Please wait
              </Button>
            </>
          ) : (
            <Button type="submit">Submit</Button>
          )}
        </form>
      </Form>
      {pendingPayments && pendingPayments.length > 0 ? (
        <Table>
          <TableHeader>
            <TableHead>Pending Payments</TableHead>
            <TableRow>
              <TableHead>Employee</TableHead>
              <TableHead>Corporation</TableHead>
              <TableHead>Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {pendingPayments.map((payment) => (
              // For each payment record, display the needed info
              // Improvement: Add an interface to type data
              <TableRow key={payment._id}>
                <TableCell className="font-medium">
                  {payment.employee.dunkin_id}
                </TableCell>
                <TableCell>
                  {payment.payor_account.payor_record.dunkin_id}
                </TableCell>
                <TableCell>{centsToDollars(payment.amount_cents)}</TableCell>
              </TableRow>
            ))}
          </TableBody>

          {loading ? (
            // Conditionally render button depending on loading state
            <>
              <Button disabled>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Please wait
              </Button>
            </>
          ) : (
            <Button
              onClick={() => processPayments(pendingPayments[0].batch_id)}
            >
              Process Payments
            </Button>
          )}
        </Table>
      ) : null}
      {showSuccess ? (
        // Notify the user that the payments were processed
        // Improvement: can create a component snackbar to display errors and success messages
        <Alert severity={"success"} icon={false}>
          Payments processes successfully!
        </Alert>
      ) : null}
    </>
  );
}
